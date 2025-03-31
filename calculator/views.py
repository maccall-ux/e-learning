from django.shortcuts import render
from .forms import ApplianceForm,BatteryCalcForm, SolarForm, GeneratorForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'calculator/home.html')


def battery(request):
    appliances = []
    total_energy = 0
    result = None
    total_watt_hours = 0
    battery_params = {}

    if request.method == 'POST':
        # Get number of appliances from hidden input
        appliance_count = int(request.POST.get('appliance_count', 0))
        
        # Process appliances
        valid = True
        for i in range(appliance_count):
            name = request.POST.get(f'appliance_{i}_name', '')
            power = request.POST.get(f'appliance_{i}_power', 0)
            quantity = request.POST.get(f'appliance_{i}_quantity', 1)
            hours = request.POST.get(f'appliance_{i}_hours', 0)

            try:
                power = float(power)
                quantity = int(quantity)
                hours = float(hours)
                watt_hours = power * quantity * hours
                
                appliances.append({
                    'name': name,
                    'power': power,
                    'quantity': quantity,
                    'hours': hours,
                    'watt_hours': watt_hours
                })
                total_watt_hours += watt_hours
            except:
                valid = False

        # Process battery parameters
        try:
            days_autonomy = float(request.POST.get('days_autonomy', 3))
            system_voltage = float(request.POST.get('system_voltage', 12))
            depth_discharge = float(request.POST.get('depth_discharge', 80)) / 100
            
            battery_params = {
                'days_autonomy': days_autonomy,
                'system_voltage': system_voltage,
                'depth_discharge': depth_discharge * 100  # Convert back to percentage for display
            }
        except:
            valid = False

        if valid and total_watt_hours > 0:
            # Calculate battery capacity
            battery_efficiency=0.8
            daily_energy = total_watt_hours / 1000  # Convert to kWh
            result = (total_watt_hours * days_autonomy) / (system_voltage * depth_discharge * battery_efficiency)
            result = round(result, 2)
            total_energy = round(daily_energy, 2)

    context = {
        'appliances': appliances,
        'total_energy': total_energy,
        'result': result,
        'total_watt_hours': total_watt_hours,
        'battery_params': battery_params,
    }
    return render(request, 'calculator/battery.html', context)

def solar_size(request):
    context = {'result': None}
    if request.method == 'POST':
        form = SolarForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            solar_wattage = (data['daily_energy'] * 1000) / (data['sun_hours'] * data['system_efficiency'])
            context['result'] = round(solar_wattage, 2)
    else:
        form = SolarForm()
    
    context['form'] = form
    return render(request, 'calculator/solar.html', context)

def generator_size(request):
    results = None
    if request.method == 'POST':
        form = GeneratorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Perform calculations
            generator_size = data['load_power'] * data['safety_factor']
            energy_required = data['load_power'] * data['runtime']
            
            results = {
                'generator_size': round(generator_size, 2),
                'energy_required': round(energy_required, 2)
            }
    else:
        form = GeneratorForm()
    
    return render(request, 'calculator/generator.html', {
        'form': form,
        'results': results
    })
