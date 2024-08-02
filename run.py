from flask import Flask, session, send_from_directory, request, render_template
from summarization import get_initial_summary, get_constrained_summary, get_multidoc_triples
from summary_evaluation import get_compression_ratio, get_coverage_ratio, get_atomic_matching_score
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management


@app.route("/")  
def index():
    return send_from_directory("THEME", "index.html") 


@app.route("/<path:name>", methods=["GET","POST"]) 
def start(name):
    return send_from_directory("THEME", name) 


def replace_quotes(s):
    return s.replace('"', "'")


@app.route("/index", methods=["POST"])
def summarize():
    session.clear()
    if request.method == 'POST':
        ## Get documents
        documents_ = request.form.getlist('summaries[]')
        documents = [replace_quotes(item) for item in documents_]

        ## Get initial summary
        processed_summary, message_list = get_initial_summary(documents)
        response_html = ''.join(processed_summary)

        ## Relation extraction
        extracted_relations, subject_list = get_multidoc_triples(documents)
        extracted_relation = [dict(t) for t in {tuple(d.items()) for d in extracted_relations}] # remove duplicates

        ## Entity clustering
        filtered_mention = [sublist for sublist in subject_list if len(sublist) > 1] 
        mention_cluster = ['( ' + ', '.join(sublist) + ' )' for sublist in filtered_mention]
    
        ## Save to session
        session['documents'] = documents
        session['message_list'] = message_list

        output = {"summary": response_html, "relation": extracted_relation ,'cluster': mention_cluster}
        return output


@app.route("/customize_summary", methods=["POST"])
def customize_summary(): 
    ## Retrieve from session
    message_list = session.pop('message_list', None)

    user_prompt = request.form.get('user_prompt')
    selected_rows_data = request.form.get('selected_rows')

    # Json to python object
    selected_rows = json.loads(selected_rows_data) 

    ## Add items to include_triple_list/exclude_triple_list
    include_triple_list = [{'subject': item['subject'], 'relation': item['relation'], 'object': item['object']} for item in selected_rows if item.get('checkboxO') == 'O']
    exclude_triple_list = [{'subject': item['subject'], 'relation': item['relation'], 'object': item['object']} for item in selected_rows if item.get('checkboxX') == 'X']

    ## Get constrained summary
    constrained_summary, message_list = get_constrained_summary(include_triple_list, exclude_triple_list, user_prompt, message_list)
    
    session['message_list'] = message_list
    summary = ''.join(constrained_summary)

    output = {"summary": summary}
    return output


@app.route("/evaluate", methods=["POST"])
def evaluate_summary(): 

    summary = request.form.getlist('output_summary')[0]

    ## Retrieve from session
    documents = session.get('documents')

    ## Evaluate
    score_compression = min(get_compression_ratio(documents, summary), 100)
    score_coverage = get_coverage_ratio(documents, summary)
    score_fact_con, statement_list = get_atomic_matching_score(documents, summary)

    output = {
        "compression": score_compression,
        'coverage': score_coverage,
        'factual_consistency': score_fact_con,
        'factual_statement_list' : statement_list
        }
    return output

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host='localhost', port=8080, debug=True) # for localhost
