import pandas as pd
import uuid  # To generate unique session IDs
from google.cloud import dialogflowcx_v3beta1 as dialogflow
import json

file_path = '/Users/saumyajain/dialogflow_env_ccap/LCC.csv'
project_id = 'ccap-gptfy-qa'
agent = '7ed2a889-bd9e-4cdc-adc5-e79f9c158528'
location = 'global'
event_name = 'start'
parameters = {

    "prompt": """Instructions:
Use the relevant fields from the JSON to find the following information:

Regional Director: {{{Regional_Director__r.Name}}}
Sales Manager:{{{Sales_Manager__r.Name}}}
""",

"Bot-Actions": {
"Bot_Actions__r" : [ {
"Name" : "#president#",
"Intent__c" : "chat indicates that the user is seeking the contact information of senior management"
}, {
"Name" : "#Can't reach staff#",
"Intent__c" : "chat indicates that the user is struggling to reach their support staff, including au pair's local office, matching specialist, customer relations manager, account manager"
}, {
"Name" : "#File a complaint#",
"Intent__c" : "chat indicates that the user would like to file a complaint against Cultural Care"
}, {
"Name" : "#Au pair needs to leave#",
"Intent__c" : "chat indicates that the user will not allow their au pair to continue staying with them"
}, {
"Name" : "#Car Accident#",
"Intent__c" : "user was involved in a road accident"
}, {
"Name" : "#Change Extension#",
"Intent__c" : "chat indicates that the user wants to change their extension length"
}, {
"Name" : "#Death#",
"Intent__c" : "chat indicates that somone died"
}, {
"Name" : "#Delayed Arrival#",
"Intent__c" : "chat indicates that someone's arrival will be delayed"
}, {
"Name" : "#Emergency#",
"Intent__c" : "chat indicates an emergency or SOS situation"
}, {
"Name" : "#Homesickness/Emotional support#",
"Intent__c" : "Chat indicates feelings of depression, home sickness, sadness, etc."
}, {
"Name" : "#Hospital#",
"Intent__c" : "identify potential medical emergencies by searching for critical phrases like \"chest pain\" or \"unconscious,\" or urgency markers like \"help!\" and \"call an ambulance!"
}, {
"Name" : "#Lost Documents#",
"Intent__c" : "chat indicates that someone lost their documents or they were stolen"
}, {
"Name" : "#Missing Au Pair#",
"Intent__c" : "chat indicates that the au pair went missing"
}, {
"Name" : "#Police#",
"Intent__c" : "chat indicates that law enforcement was involved"
}, {
"Name" : "#Program Counselor#",
"Intent__c" : "chat indicates that the user wants to speak to a program counselor or expresses the need for mental health services. Only consider with high confidence and do not consider queries simply asking who the Program Manager is."
}, {
"Name" : "#Return early#",
"Intent__c" : "chat indicates that an au pair is returning early, not continuing with the program"
}, {
"Name" : "#Visa Rejection#",
"Intent__c" : "chat indicates that someone's visa was rejected"
}, {
"Name" : "#Password Reset#",
"Intent__c" : "chat indicates a user was attempting to reset their password and password and failing"
}, {
"Name" : "#LCC Change#",
"Intent__c" : "Chat indicates user would like to be reassigned to a different LCC or they don't want to work with their LCC anymore. Do not consider if they ask who their LCC is."
}, {
"Name" : "#Wrong Pay#",
"Intent__c" : "user indicates that their pay was wrong"
}, {
"Name" : "#Reduce group size#",
"Intent__c" : "user indicates they want to reduce their working hours, reduce the group of customers they support, or change their work status with cultural care from full time to part time"
}, {
"Name" : "#Who is LCC#",
"Intent__c" : "user wants to know who the LCC for a particular area (city, town, state, zip code) is"
}, {
"Name" : "#Add spouse as LCC#",
"Intent__c" : "chat indicates that LCC would like to add their husband, wife or spouse as a an LCC"
}, {
"Name" : "#Name change#",
"Intent__c" : "chat indicates that the user wants to change their name"
}, {
"Name" : "#Gibberish#",
"Intent__c" : "any user query that's not a valid word or random characters such as .,-afhaf"
}, {
"Name" : "#Agent#",
"Intent__c" : "There is no answer found for the chat question. Customer seems to be agitated or indicates to be connected to a staff member or representative."
}, {
"Name" : "#Help#",
"Intent__c" : "User asks for help or is confused"
}, {
"Name" : "#Timeout#",
"Intent__c" : None
}, {
"Name" : "#Testing",
"Intent__c" : "Detect if the user says \"Testing\" or #testing."
}, {
"Name" : "#Feedback",
"Intent__c" : "Detect if the user says \"Feedback\" or #feedback."
}, {
"Name" : "#Legal#",
"Intent__c" : "chat indicates a legal issue or need to speak to a lawyer/ attorney"
}, {
"Name" : "#Assault#",
"Intent__c" : "chat indicates that there was a situation of assault or harrassment"
}, {
"Name" : "#Arrest#",
"Intent__c" : "Chat indicates that there is a situation of someone getting arrested by law enforcement."
}, {
"Name" : "#Address Change#",
"Intent__c" : "Chat indicates that there is a need for an address to be updated, including if an au pair alerts that their host family has moved"
}, {
"Name" : "#Stuck at Border#",
"Intent__c" : "chat indicates that someone is unable to cross the border"
} ],
"Object Name" : "Bot_Configuration__c",
"Id" : "a6JDQ000000KzPG2A0"
},

"SFJsonObject": {
"Object Name": "Contact",
"Regional_Director__r.Name": "Saumya",
"Sales_Manager__r.Name": "Sagar"
}

}

def detect_intent_text(project_id, location, agent, session_id, event_name, parameters, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, location, agent, session_id)

    event_input = dialogflow.EventInput(event=event_name)
    parameters = dialogflow.QueryParameters(parameters=parameters)
    event_query_input = dialogflow.QueryInput(event=event_input, language_code='en')

    session_client.detect_intent(
        request={"session": session, "query_input": event_query_input, "query_params":parameters}
    )

    text_input = dialogflow.TextInput(text=text)
    query_input = dialogflow.QueryInput(text=text_input, language_code='en')

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    response_text = response.query_result.response_messages[0].text.text
    # response_payload = response.query_result.response_messages[0].payload
    response_body = response.query_result
    response_body_str = str(response.query_result)

    file_path = "response_text.txt"

    # Write the response text to the text file
    with open(file_path, "w") as file:
        file.write(response_body_str)

    print("Response text saved to response_text.txt")
         

    
    return response_text, response_body


# Load CSV file into a DataFrame
df = pd.read_csv(file_path)

# Create a new DataFrame to store the preprocessed data
new_rows = []

# Iterate through each row in the DataFrame and preprocess the questions
for index, row in df.iterrows():
        questions = row['question'].split('<br>')
        old_answer = row['answer']
        for q in questions:
            new_rows.append({'question': q, 'answer': old_answer})

# Create a new DataFrame from the preprocessed data
preprocessed_df = pd.DataFrame(new_rows)

# Set up an empty DataFrame to store the results
result_df = pd.DataFrame(columns=['Question', 'FAQ Answer'])

# Iterate through each row in the preprocessed DataFrame
for index, row in preprocessed_df.iterrows():
    question = row['question']
    old_answer = row['answer']
    
    # Generate a unique session ID for each question
    session_id = str(uuid.uuid4())

    # Hit the API for each question in a new session
    response_text, response_body = detect_intent_text(project_id, agent=agent, location=location, session_id=session_id, text=question, event_name=event_name, parameters=parameters)
    
    # Append the question and corresponding answer to the result DataFrame
    result_df = result_df._append({'Question': question, 'FAQ Answer': old_answer,'Response Text': response_text, 'Response Body': response_body}, ignore_index=True)
    # result_df = result_df._append(
    #         {'Question': question, 'FAQ Answer': old_answer, 'Bot Response': response["answers"], 'NOT_ENOUGH_INFORMATION': response["NOT_ENOUGH_INFORMATION"], 'SessionId': response["sessionId"], "Response Not Fetched From FAQ": response["RespNotFetteched"]}, ignore_index=True)

# Display the result DataFrame
print(result_df)

# Save the result DataFrame to a new CSV file
result_df.to_csv('dialogflow_results.csv', index=False)



# parse the response body to retrieve "NOT_ENOUGH_INFORMATION"

with

