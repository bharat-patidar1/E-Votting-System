import pandas as pd

data = {
    'VoterID': ['VOTER001', 'VOTER002', 'VOTER003', 'VOTER004', 'VOTER005'],
    'Name': ['Rahul Sharma', 'Priya Singh', 'Amit Patel', 'Sneha Verma', 'Vikram Yadav'],
    'Password': ['pass123', 'pass123', 'pass123', 'pass123', 'pass123']
}

df = pd.DataFrame(data)
df.to_excel('voter_data.xlsx', index=False)
print("voter_data.xlsx generated successfully.")
