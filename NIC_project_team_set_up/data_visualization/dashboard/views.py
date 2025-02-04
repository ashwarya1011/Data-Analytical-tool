
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Jjm,  FinancingOfGrossFiscalDeficit, Pmjdy,  RuralHealthStatistics
# importing the models to perform database operations
import plotly.express as px
from plotly.io import to_json
from plotly.offline import plot
from plotly.graph_objs   import  Figure
import h2o
from h2o.automl import H2OAutoML
import pandas as pd
import numpy as np

def index(request):
    return render(request, 'index.html')

def get_states(request):
    dataset = request.GET.get('dataset')
    selected_state = request.GET.get('state')

    states = []

    if dataset == 'Jjm':
        states = Jjm.objects.values_list('states', flat=True).distinct()
        financial_years = Jjm.objects.values_list('fy', flat=True).distinct()
    elif dataset == 'FinancingOfGrossFiscalDeficit':
        states = []
        financial_years = FinancingOfGrossFiscalDeficit.objects.values_list('srcyear', flat=True).distinct()
    elif dataset == 'Pmjdy':
        states = Pmjdy.objects.values_list('srcstatename', flat=True).distinct()
        financial_years = Pmjdy.objects.values_list('srcyear', flat=True).distinct()
    elif dataset == 'RuralHealthStatistics':
        states = RuralHealthStatistics.objects.values_list('srcstatename', flat=True).distinct()
        financial_years = RuralHealthStatistics.objects.values_list('srcyear', flat=True).distinct()

    return JsonResponse({'states': list(states), 'financial_years': list(financial_years)})

def get_kpis(request):
    dataset = request.GET.get('dataset')

    model = None 

    if dataset == 'Jjm':
        model = Jjm
    elif dataset == 'FinancingOfGrossFiscalDeficit':
        model = FinancingOfGrossFiscalDeficit
    elif dataset == 'Pmjdy':
        model = Pmjdy
    elif dataset == 'RuralHealthStatistics':
        model = RuralHealthStatistics

    if model is not None:
        kpis = [field.name for field in model._meta.get_fields() if field.name not in ['id', 'states', 'districts', 'srcstatename', 'srcdistrictname', 'srcyear', 'fy', 'year', 'yearcode', 'country', ]]
        return JsonResponse({'kpis': kpis})
    else:
        return JsonResponse({'error': 'Invalid dataset'}, status=400)

def process_form(request):
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                dataset = data.get('dataset')
                state = data.get('state')
                financial_years = data.get('financial_years')
                kpi = data.get('kpis')
                action = data.get('action')  # Separate action for visualizations and insights
                plot_types = data.get('plot_types', [])  # Retrieve selected plot types
                print(dataset, state, financial_years, kpi, action)

                df = pd.DataFrame()

                model = None
                group_by_field = 'fy'

                if dataset == 'Jjm':
                    
                    queryset = Jjm.objects.all()
                    if state != 'All':
                        queryset = queryset.filter(states=state)
                        
                    if financial_years != 'All':
                        queryset = queryset.filter(fy__in=financial_years)

                elif dataset == 'FinancingOfGrossFiscalDeficit':
                    queryset = FinancingOfGrossFiscalDeficit.objects.all()
                    if financial_years != 'All':
                        queryset = queryset.filter(srcyear__in=financial_years)
 
                    group_by_field = 'srcyear'  

                elif dataset == 'Pmjdy':
                    queryset = Pmjdy.objects.all()
                    if state != 'All':
                        queryset = queryset.filter(srcstatename=state)
 
                    if financial_years != 'All':
                        queryset = queryset.filter(srcyear__in=financial_years)
  
                    group_by_field = 'srcyear'

                elif dataset == 'RuralHealthStatistics':
                    queryset = RuralHealthStatistics.objects.all()
                    if state != 'All':
                        queryset = queryset.filter(srcstatename=state)
 
                    if financial_years != 'All':
                        queryset = queryset.filter(srcyear__in=financial_years)

                    group_by_field = 'srcyear'
                else:
                    return JsonResponse({'error': 'Invalid dataset selected'}, status=400)

           

                df = pd.DataFrame(list(queryset.values(group_by_field, kpi)))
               

                # Ensure KPI column is numeric
                df[kpi] = pd.to_numeric(df[kpi], errors='coerce')
              

                # Handle NaNs by filling them with 0
                df.fillna(0, inplace=True)  
                # Or df.dropna(inplace=True)
             
                #Group by financial year and sum the KPI values
                df_grouped = df.groupby(group_by_field)[kpi].sum().reset_index()
                print(df_grouped)
             


                

                
                #processing data and generating insights
                if 'generate_insights' in action:
                    
                    # Calculate mean and median for the selected KPI
                    mean_kpi = df_grouped[kpi].mean()
                    median_kpi = df_grouped[kpi].median()

                    # Trend Analysis
                    trend_data = df_grouped.copy()
                    trend_data['time_index'] = trend_data[group_by_field].apply(lambda x: int(x.split('-')[0]))
                    trend_slope = np.polyfit(trend_data['time_index'], trend_data[kpi], 1)[0]  # Calculate the slope

                    if trend_slope > 0:
                        trend = "increasing"
                    elif trend_slope < 0:
                        trend = "decreasing"
                    else:
                        trend = "stable"
                    # Growth Rate Calculation
                    first_value = df_grouped[kpi].iloc[0]
                    last_value = df_grouped[kpi].iloc[-1]


                    # Check if first_value is zero to avoid division by zero
                    if first_value != 0:
                        overall_growth_rate = ((last_value - first_value) / first_value) * 100
                        if overall_growth_rate > 0:
                            growth_trend = f"increased by {overall_growth_rate:.2f}%"
                        elif overall_growth_rate < 0:
                            growth_trend = f"decreased by {abs(overall_growth_rate):.2f}%"
                        else:
                            growth_trend = "remained stable"
                    else:
                        growth_trend = "Can't be computed (first value is zero)"

                    df_grouped['time_index'] = df_grouped[group_by_field].apply(lambda x: int(x.split('-')[0]))

                    # Predict the next period using a time series model
                    h2o.init()
                    filtered_data = h2o.H2OFrame(df_grouped)
                    predictions = {}
                    best_models = {}

                    next_prediction_results = ""
                    # scenario_analysis_results = ""


                    response = kpi
                    predictors = filtered_data.columns.remove(response)

                    # Run AutoML for automatic model selection and training
                    aml = H2OAutoML(max_models=10, seed=1, max_runtime_secs=1200, nfolds=len(financial_years),keep_cross_validation_predictions=True)
                    aml.train(x=predictors, y=response, training_frame=filtered_data)

                    # Get the best model and make predictions
                    best_model = aml.leader

                    # Predict for the next period
                    unique_fy = df_grouped[group_by_field].unique()
                    next_period_data = pd.DataFrame({'FY': [unique_fy[-1]]})
                    next_period_data['time_index'] = int(unique_fy[-1].split('-')[0]) + 1

                    # Create a future_frame with the last row values plus the next period
                    last_row = df_grouped.iloc[-1].to_dict()
                    next_row = {**last_row, 'FY': next_period_data['FY'].values[0], 'time_index': next_period_data['time_index'].values[0]}
                    next_frame = h2o.H2OFrame(pd.DataFrame([next_row]))

                    # Predict on the next period data
                    next_prediction = best_model.predict(next_frame)
                    predictions[kpi] = next_prediction
                    best_models[kpi] = best_model

                    # Append the predicted value to results
                    next_prediction_results = f"({next_period_data['FY'].values[0]}): {next_prediction[0, 0]:.2f}"

                    h2o.cluster().shutdown()

                    insights = {
                    'dataset': dataset,
                    'state': state,
                    'kpi': kpi,
                    'mean_kpi': mean_kpi,
                    'median_kpi': median_kpi,
                    'trend': trend,
                    'growth_trend': growth_trend,
                    'next_prediction_results': next_prediction_results,
                    # 'scenario_analysis_results':scenario_analysis_results
                    }

                    print(insights)

                    return JsonResponse({'insights': insights})
                
                elif 'visualize' in action:

                    # Generate Plotly figures based on action
                    plots = []
                    if 'line_plot' in plot_types:
               
                        fig = px.line(df_grouped, x=group_by_field, y=kpi, title=f"Line Plot of {kpi} by Financial Year")
                
                        plots.append(to_json(fig))
                      
                    if 'bar_plot' in plot_types:
                        fig = px.bar(df_grouped, x=group_by_field, y=kpi, title=f"Bar Plot of {kpi} by Financial Year")
                        plots.append(to_json(fig))
                    if 'scatter_plot' in plot_types:
                        fig = px.scatter(df_grouped, x=group_by_field, y=kpi, title=f"Scatter Plot of {kpi} by Financial Year")
                        plots.append(to_json(fig))
                    if 'pie_chart' in plot_types:
                        fig = px.pie(df_grouped, names=group_by_field,values=kpi, title=f"Pie Chart of {kpi} by Financial Year")
                        plots.append(to_json(fig))
                    if 'box_plot' in plot_types:
                        fig = px.box(df_grouped, x=group_by_field, y=kpi, title=f"Box Plot of {kpi} by Financial Year")
                        plots.append(to_json(fig))
                    if 'histogram' in plot_types:
                        fig = px.histogram(df_grouped, x=group_by_field, y=kpi, title=f"Histogram of {kpi} by Financial Year")
                        plots.append(to_json(fig))
                    # Return the generated plots to the frontend
                    return JsonResponse({'plots': plots})
            except Exception as e:
                return JsonResponse({'error' : str(e)}, status=500)
        
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    
