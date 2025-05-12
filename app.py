import streamlit as st
import datetime
import base64
from fpdf import FPDF
import io
import math

st.set_page_config(page_title="Life Insurance Calculator", layout="wide")

# Function to create and download PDF
def create_download_link(val, filename):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">Download PDF Report</a>'

def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Set up the PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Life Insurance Calculator Report", ln=True, align="C")
    pdf.line(10, 22, 200, 22)
    pdf.ln(5)
    
    # Client Information
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Client Information", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(50, 8, f"Client Name: {data['client_name']}", ln=True)
    pdf.cell(50, 8, f"Date: {data['date']}", ln=True)
    pdf.cell(50, 8, f"Beneficiary: {data['beneficiary']}", ln=True)
    
    # Add inflation info if it was used
    if data['inflation_used']:
        pdf.cell(50, 8, f"Inflation Rate: {data['inflation_rate']}%", ln=True)
    pdf.ln(5)
    
    # Income Needs
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Income Needs", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(190, 8, f"1. Annual income needed: ${data['line1']:,.2f}", ln=True)
    pdf.cell(190, 8, f"2. Annual income from other sources: ${data['line2']:,.2f}", ln=True)
    pdf.cell(190, 8, f"3. Annual income to be replaced: ${data['line3']:,.2f}", ln=True)
    pdf.cell(190, 8, f"4. Funds needed to provide income ({data['years']} years): ${data['line4']:,.2f}", ln=True)
    pdf.ln(5)
    
    # Expenses
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Expenses", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(190, 8, f"5. Burial final expenses: ${data['line5']:,.2f}", ln=True)
    pdf.cell(190, 8, f"6. Mortgage and other debts: ${data['line6']:,.2f}", ln=True)
    pdf.cell(190, 8, f"7. College costs: ${data['line7']:,.2f}", ln=True)
    pdf.cell(190, 8, f"8. Total capital required: ${data['line8']:,.2f}", ln=True)
    pdf.ln(5)
    
    # Assets
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Assets", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(190, 8, f"9. Savings and investments: ${data['line9']:,.2f}", ln=True)
    pdf.cell(190, 8, f"10. Retirement savings: ${data['line10']:,.2f}", ln=True)
    pdf.cell(190, 8, f"11. Present amount of life insurance: ${data['line11']:,.2f}", ln=True)
    pdf.cell(190, 8, f"12. Total of all assets: ${data['line12']:,.2f}", ln=True)
    pdf.ln(5)
    
    # Result
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Result", ln=True)
    pdf.set_font("Arial", "B", 11)
    if data['line13'] > 0:
        pdf.cell(190, 8, f"Additional life insurance needed: ${data['line13']:,.2f}", ln=True)
    else:
        pdf.cell(190, 8, f"Sufficient coverage with surplus: ${abs(data['line13']):,.2f}", ln=True)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "This is an estimate only. Please consult with a financial advisor for a comprehensive plan.", 0, 0, "C")
    
    return pdf.output(dest="S").encode("latin-1")

# Function to calculate inflation-adjusted value
def calculate_with_inflation(base_value, inflation_rate, years):
    return base_value * math.pow(1 + (inflation_rate/100), years)

# Create tabs for better organization
tab1, tab2 = st.tabs(["Calculator", "About"])

with tab1:
    st.title("Life Insurance Calculator")
    st.write("Complete the fields below to estimate your life insurance needs.")
    
    # Add inflation option
    use_inflation = st.checkbox("Factor in inflation (based on Consumer Price Index)", value=False)
    
    if use_inflation:
        inflation_rate = st.slider(
            "Annual inflation rate (%)", 
            min_value=1.0, 
            max_value=10.0, 
            value=2.5, 
            step=0.1,
            help="The Consumer Price Index (CPI) is used as the inflation metric, as it measures general price level changes that affect cost of living."
        )
        st.info(f"Calculations will be adjusted for inflation at {inflation_rate}% annually.")
    else:
        inflation_rate = 0.0
    
    # Use expanders for each section to make the UI cleaner
    with st.expander("Client Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("Client Name", value="John Smith")
        with col2:
            date = st.date_input("Date", value=datetime.date.today())
        
        beneficiary = st.text_input("Beneficiary", value="Sally Smith")
    
    with st.expander("Income Needs", expanded=True):
        # Line 1: Annual income needed
        line1 = st.number_input(
            "1. Annual income your family will need if you die today ($)",
            min_value=0.0,
            value=100000.0,
            help="Enter a number that is 60-80% of gross income, including salaries, dividends, interest, etc."
        )
        
        # Line 2: Annual income from other sources
        line2 = st.number_input(
            "2. Annual income available to your family from other sources ($)",
            min_value=0.0,
            value=0.0,
            help="Enter a number that includes dividends, interest, spouse's earnings and social security."
        )
        
        # Line 3: Annual income to be replaced
        line3 = line1 - line2
        st.write(f"3. Annual Income to be replaced: ${line3:,.2f}")
        
        # Line 4: Funds needed based on years
        st.write("4. Funds needed to provide income")
        
        year_factors = {
            10: 8.9,
            15: 12.4,
            20: 15.4,
            25: 18.1,
            30: 20.4,
            35: 22.4,
            40: 24.1,
            45: 25.6,
            50: 26.9,
            55: 28.1,
            60: 29.0
        }
        
        years = st.selectbox(
            "Number of years to provide income",
            options=list(year_factors.keys()),
            index=2  # Default to 20 years
        )
        
        factor = year_factors[years]
        
        # Apply inflation if selected
        if use_inflation:
            # Calculate the average annual income needed over the period with inflation
            inflated_line3 = 0
            for year in range(1, years + 1):
                inflated_line3 += calculate_with_inflation(line3, inflation_rate, year)
            average_inflated_line3 = inflated_line3 / years
            line4 = average_inflated_line3 * factor
            st.write(f"Average annual income needed (with inflation): ${average_inflated_line3:,.2f}")
        else:
            line4 = line3 * factor
            
        st.write(f"Factor for {years} years: {factor}")
        st.write(f"Funds needed (line 3 × factor): ${line4:,.2f}")
    
    with st.expander("Expenses", expanded=True):
        # Line 5: Burial and final expenses
        line5 = st.number_input(
            "5. Burial final expenses, emergency fund ($)",
            min_value=0.0,
            value=10000.0,
            help="The average cost of an adult funeral is $10,000"
        )
        
        # Line 6: Mortgage and other debts
        line6 = st.number_input(
            "6. Mortgage and other debts ($)",
            min_value=0.0,
            value=250000.0,
            help="Include mortgage balance, credit card debt, car loans, home equity loans, etc."
        )
        
        # Line 7: College costs
        st.write("7. College costs")
        st.write("2005-2006 average annual cost of a 4 year education: public-$15,566; private-$31,916.")
        
        college_costs = []
        total_college_cost = 0.0
        
        num_children = st.number_input("Number of children for college", min_value=0, max_value=10, value=0)
        
        if num_children > 0:
            for i in range(int(num_children)):
                col1, col2 = st.columns(2)
                with col1:
                    annual_cost = st.number_input(f"Annual college cost for Child {i+1} ($)", 
                                                min_value=0.0, 
                                                value=15566.0,  # Default to public cost
                                                key=f"cost_{i}")
                with col2:
                    years_college = st.number_input(f"Years of college for Child {i+1}", 
                                                  min_value=1, 
                                                  max_value=8, 
                                                  value=4, 
                                                  key=f"years_{i}")
                    # When does college start for this child?
                    years_until_college = st.number_input(f"Years until Child {i+1} starts college", 
                                                       min_value=0, 
                                                       max_value=25, 
                                                       value=0,
                                                       key=f"until_college_{i}")
                
                # Apply inflation to college costs if selected
                if use_inflation and years_until_college > 0:
                    inflated_annual_cost = calculate_with_inflation(annual_cost, inflation_rate, years_until_college)
                    st.write(f"Inflated annual cost in {years_until_college} years: ${inflated_annual_cost:,.2f}")
                    child_total = inflated_annual_cost * years_college
                else:
                    child_total = annual_cost * years_college
                
                college_costs.append(child_total)
                st.write(f"Total for Child {i+1}: ${child_total:,.2f}")
                total_college_cost += child_total
        
        line7 = total_college_cost
        st.write(f"Total College Costs: ${line7:,.2f}")
        
        # Line 8: Total Capital Required
        line8 = line4 + line5 + line6 + line7
        st.write(f"8. Total Capital Required: ${line8:,.2f}")
    
    with st.expander("Assets", expanded=True):
        # Line 9: Savings and Investments
        line9 = st.number_input(
            "9. Savings and Investments ($)",
            min_value=0.0,
            value=50000.0,
            help="Bank accounts, CDs, stocks, bonds, mutual funds, real estate, rental properties, etc."
        )
        
        # Line 10: Retirement savings
        line10 = st.number_input(
            "10. Retirement savings ($)",
            min_value=0.0,
            value=250000.0,
            help="IRAs, 401(k), SEPs, Pension and profit sharing plans"
        )
        
        # Line 11: Present amount of life insurance
        line11 = st.number_input(
            "11. Present amount of life insurance ($)",
            min_value=0.0,
            value=150000.0,
            help="Include both personal as well as group insurance"
        )
        
        # Line 12: Total of all assets
        line12 = line9 + line10 + line11
        st.write(f"12. Total of all assets: ${line12:,.2f}")
        
        # Line 13: Estimated amount of additional life insurance needed
        line13 = line8 - line12
        
        # Partner coverage
        partner_coverage = st.number_input(
            "How much coverage does your spouse/business partner have? ($)",
            min_value=0.0,
            value=0.0
        )
    
    # Results section
    st.header("Results Summary")
    
    # Use columns for a cleaner layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Needs")
        needs_data = [
            {"item": "Income funds needed", "amount": line4},
            {"item": "Burial expenses", "amount": line5},
            {"item": "Debts", "amount": line6},
            {"item": "College costs", "amount": line7}
        ]
        needs_df = st.dataframe(needs_data, hide_index=True, 
                             column_config={"item": "Category", "amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f")})
        
        st.metric("Total capital required", f"${line8:,.2f}")
    
    with col2:
        st.subheader("Assets")
        assets_data = [
            {"item": "Savings & Investments", "amount": line9},
            {"item": "Retirement savings", "amount": line10},
            {"item": "Current life insurance", "amount": line11}
        ]
        assets_df = st.dataframe(assets_data, hide_index=True,
                              column_config={"item": "Category", "amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f")})
        
        st.metric("Total assets", f"${line12:,.2f}")
    
    # Show inflation information in the results if used
    if use_inflation:
        st.info(f"Results include inflation adjusted at {inflation_rate}% annually based on the Consumer Price Index (CPI).")
    
    st.subheader("Result")
    if line13 > 0:
        st.success(f"Additional life insurance needed: ${line13:,.2f}")
    else:
        st.success(f"You have sufficient life insurance coverage with a surplus of ${abs(line13):,.2f}")
    
    # Generate PDF section
    st.header("Generate Report")
    
    if st.button("Generate PDF Report"):
        data = {
            'client_name': client_name,
            'date': date.strftime('%Y-%m-%d'),
            'beneficiary': beneficiary,
            'inflation_used': use_inflation,
            'inflation_rate': inflation_rate if use_inflation else 0,
            'line1': line1,
            'line2': line2,
            'line3': line3,
            'line4': line4,
            'years': years,
            'line5': line5,
            'line6': line6,
            'line7': line7,
            'line8': line8,
            'line9': line9,
            'line10': line10,
            'line11': line11,
            'line12': line12,
            'line13': line13,
            'partner_coverage': partner_coverage
        }
        pdf = create_pdf(data)
        html = create_download_link(pdf, f"Life_Insurance_Report_{client_name.replace(' ', '_')}.pdf")
        st.markdown(html, unsafe_allow_html=True)

with tab2:
    st.title("About This Calculator")
    st.write("""
    This calculator provides a quick and simple method to estimate the amount of life insurance you will need.
    
    ### How to Use
    1. Fill out your personal information
    2. Enter your income needs
    3. List your expenses including burial costs, debts, and college expenses
    4. Enter your current assets
    5. Get an instant calculation of your life insurance needs
    6. Generate and download a PDF report
    
    ### Inflation Adjustment
    The calculator allows you to factor in inflation using the Consumer Price Index (CPI) as the inflation metric. 
    When enabled, this will adjust future expenses and income needs based on the selected inflation rate.
    
    ### Sending to Clients
    You can send the link to this app to your clients for them to complete themselves. 
    After they fill in their information, they can download the PDF report and send it back to you.
    
    ### Notes
    - This is a simplified calculation and should be used as a starting point for discussion
    - For a comprehensive financial plan, please consult with a qualified financial advisor
    - All information entered is private and not stored on any server
    """)

    st.info("For advisors: You can bookmark and share this URL with your clients.") 