import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm
from django.core.mail import EmailMessage

def upload_file(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)

            # Generate summary data
            summary_data = generate_summary(df)

            # Send email
            send_summary_email(summary_data)

            return render(request, 'upload/success.html', {'summary': summary_data})

    return render(request, 'upload/upload.html')

def generate_summary(df):
    # Group by 'Cust State' and 'Cust Pin', counting occurrences of each
    summary = df.groupby(['Cust State', 'Cust Pin']).size().reset_index(name='Count')
    # Rename columns to remove spaces
    summary.columns = ['Cust_State', 'Cust_Pin', 'Count']
    # Filter for counts greater than 1 if needed
    filtered_summary = summary[summary['Count'] > 1]
    return filtered_summary.to_dict(orient='records')

def send_summary_email(summary_data):
    # Create plain text summary
    summary_text = "Cust State\tCust Pin\tCount\n"
    
    for row in summary_data:
        summary_text += f"{row['Cust_State']}\t{row['Cust_Pin']}\t{row['Count']}\n"
    
    # Send email
    email = EmailMessage(
        subject='Python Assignment - Anurag',
        body=summary_text,
        from_email='anurag21xxx005@akgec.ac.in',  # Replace with your email
        to=['tech@themedius.ai'],
    )
    
    email.send()
