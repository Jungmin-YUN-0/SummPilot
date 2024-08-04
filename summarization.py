import re
import json
import openai
from tqdm.auto import tqdm

# Please enter your api key
#openai.api_key = "your_openai_api_key_here"

stop_list = ['it', 'his', 'her', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

def get_initial_summary(article_list: list):
    """
    Get initial summary from gpt.
    """
    input_article = "\n".join([f"[Article {i+1}]\n{article}\n\n" for i, article in enumerate(article_list)])+'\n'
    
    message_list = [
        {"role": "system", "content": "You are a helpful assistant. \
Your job is to summarize given documents. \
Do not generate chat-style responses such as \"Sure!\", \"Here's the output\"."
        },
        {"role": "user", "content": "Please summarize multiple documents into a single, concise document.\n \
Exclude any unrelated noisy content, such as advertisements, etc.\n\
Format the output as follows:\n\n[Summary]\nContent\n"
        },
        {"role": "user", "content": "[Article1]\n \
The Portland Golf Club is a private golf club in the northwest United States, in suburban Portland, Oregon. The PGC is located in the unincorporated Raleigh Hills area of eastern Washington County, southwest of downtown Portland and east of Beaverton. \n\n \
[Article2]\n \
PGC was established in the winter of 1914, when a group of nine businessmen assembled to form a new club after leaving their respective clubs. The golf club hosted the Ryder Cup matches of 1947, the first renewal in a decade, due to World War II. The U.S. team defeated Great Britain 11 to 1 in wet conditions in early November."
        },
        {"role": "assistant", "content": "[Summary]\n \
The Portland Golf Club, or PGC, is a private golf club located in the northwest United States, in suburban Portland, Oregon. Established in 1914 by nine businessmen, it hosted the 1947 Ryder Cup matches where the U.S. team defeated Great Britain 11 to 1 in wet conditions."
        },    
    ]
    message_list.append({"role": "user", "content": input_article})

    max_errors = 5
    error_counter = 0
    while error_counter < max_errors:
        try:
            # Get gpt response
            gpt_response, message_list = get_response(message_list, attach=False)

            # Assert that the response has the desired format
            checker = gpt_response.split("\n", 2)
            if checker[0] != "[Summary]":
                raise AssertionError(f"Expected [Summary] in the first line but got {checker[0]}")
            elif len(checker) > 2:
                raise AssertionError(f"Expected only one line after [Summary] but got {len(checker)-1} lines")

            break   # If everything is fine, break the loop
        except Exception as e:
            error_counter += 1
            if error_counter >= max_errors:
                raise RuntimeError("Too many errors. Please restart the program.")

    message_list.append({"role": "assistant", "content": gpt_response})

    init_summary = checker[1]
    return init_summary, message_list


def get_constrained_summary(include_triple_list: list, exclude_triple_list: list, custom_prompt: str, message_list: list):
    requirements_list = parse_requirements(include_triple_list, "include") + parse_requirements(exclude_triple_list, "exclude")
    if custom_prompt != "":
        requirements_list.append(custom_prompt)

    requirements_message = "Thank you. Please address the following requests in your summary.\n\n"
    for requirement in requirements_list:
        requirements_message += "* " + requirement + "\n"
    requirements_message += "\n\nFormat the output as follows:\n\n[Summary]\nContent"

    message_list.append({"role": "user", "content": requirements_message})

    error_counter = 0
    while True:
        try:
            # Get gpt response
            gpt_response, message_list = get_response(message_list, attach=False)

            # Assert that the response has desired format
            checker = gpt_response.split("\n")
            if checker[0] != "[Summary]":
                raise AssertionError(f"Expected [Summary] in the first line but got {checker[0]}")
            elif len(checker) > 2:
                raise AssertionError(f"Expected only one line after [Summary] but got {len(checker)-1} lines")

            break # if everything is fine, break the loop
        except:
            error_counter += 1
            if error_counter > 5:
                raise RuntimeError("Too many errors. Please restart the program.")
            else:
                continue

    message_list.append({"role": "assistant", "content": gpt_response})

    final_summary = checker[1]
    return final_summary, message_list


def parse_requirements(triple_list: list, type: str) -> list:
    requirement_list = []
    for triple in triple_list:
        if type == "include":   
            requirement_list.append(f"Ensure that the summary includes content related to the triple {triple['subject']}-{triple['relation']}-{triple['object']}.")
        elif type == "exclude":
            requirement_list.append(f"Please remove any content related to the triple {triple['subject']}-{triple['relation']}-{triple['object']}.")
    return requirement_list


def get_response(message_list: list, attach=True):
    """
    Simple wrapper to get response from gpt.
    """
    gpt_response = openai.ChatCompletion.create(
        #model='gpt-4-1106-preview',
        model = 'gpt-4o',
        messages=message_list,
        max_tokens=2048
    )

    response = gpt_response['choices'][0]['message']['content']

    if attach:
        message_list.append({
            "role": "assistant",
            "content": response
        })

    return response, message_list


def get_extracted_triples(document: str) -> list:
    input_document = f"[Document]\n{document}\n\n"
    
    message_list = [
        {"role": "system", "content": "You are a helpful assistant. \
Your job is to extract relation triples from given documents. \
Do not generate chat-style responses such as \"Sure!\", \"Here's the output\"."
        },
        {"role": "user", "content": "Please extract important and concise relational triples from the document. Identify relationships between each pair of entities. \
Each triple consists of a subject, a relation, and an object.\n \
Ensure that both the subject and object are limited to four words each. Express the triple as concisely as possible.\n \
The output format should be as follows :\n\n[Relation triples]\n * <subject|relation|object>\n * <subject|relation|object>\n * <subject|relation|object>\n"
        },
        {"role": "user", "content": "I'll show you an example"},
        {"role": "user", "content": "[Document]\n \
The Portland Golf Club is a private golf club located in the United States. PGC was established in 1914 by nine businessmen from the U.S."
        },
        {"role": "user", "content": "[Relation triples]\n * <Portland Golf Club|is located in|United States>\n * <PGC|was established in|1914>\n * <PGC|was established by|nine businessmen>\n * <nine businessmen|are from|U.S>\n"},
        {"role": "user", "content": "Now, I'll give you documents."}
    ]
    
    message_list.append({"role": "user", "content": input_document})
    
    error_counter = 0
    triple_list = []
    while True:
        try:
            # Get gpt response
            gpt_response, message_list = get_response(message_list, attach=False)

            # Assert that the response has desired format
            checker = gpt_response.split("\n")
            if checker[0] != "[Relation triples]":
                raise AssertionError(f"Expected [Relation triples] in the first line but got {checker[0]}")

            for line in checker[1:]:
                line = line.rstrip(">").lstrip("* <")
                triple = line.split("|")
                if len(triple) != 3:
                    raise AssertionError(f"Expected 3 elements in a triple but got {len(triple)} elements")
                else:
                    triple = {"subject": triple[0], "relation": triple[1], "object": triple[2]}
                    triple_list.append(triple)

            break # if everything is fine, break the loop
        except:
            error_counter += 1
            if error_counter > 5:
                raise RuntimeError("Too many errors. Please restart the program.")
            else:
                continue

    message_list.append({"role": "assistant", "content": gpt_response})

    return triple_list, message_list


def get_clustered_entity(message_list: list) -> list:
    assert message_list != []
    
    message_list.append(
        {"role": "user",
        "content": f"Thank you. Please perform coreference resolution on the entities extracted from the triple. An entity includes a subject and an object, not a relation.\n\n\
* Coreference resolution is the task of identifying and linking different noun phrases (mentions) that represents the same entity.\n\
* Group together the multiple noun phrases that represents the same entity into one triples.\n\
### * For example, since 'Los Angeles' and 'L.A.' represents same entity, you should group them together. If 'Jordan' and 'Michael Jordan' represents same entity, you should group them.\n\
* Read the given document, identify coreferences for the subject and object of the extracted triple, and combine them into a single triple. \
* For example, if you have <Los Angeles|Located in|California> in the generated triple list and L.A. in the document, combine them into <[Los Angeles+L.A.]|Located in|California>.\n\
* If you couldn't find any coreference, please leave it as it is. Print the original triple in this case.\n\
* Output the results in the following format:\n\n\
[Coreference Resolution]\n\
* <[Subject1a+Subject1b]|Relation1|Object1>\n\
* <[Subject2a+Subject2b+Subject2c]|Relation2|Object2>\n\
* <Subject3|Relation3|[Object3a+Object3b]>"
        }
    )
    
    error_counter = 0
    while True:
        try:
            # Get gpt response
            gpt_response, message_list = get_response(message_list, attach=False)

            # Assert that the response has desired format
            cluster_extracted = gpt_response.split("\n")
            if cluster_extracted[0] != "[Coreference Resolution]":
                raise AssertionError(f"Expected [Coreference Resolution] in the first line but got {cluster_extracted[0]}")

            cluster_list = []
            for i in range(1, len(cluster_extracted)):
                line = cluster_extracted[i]
                assert line[:3] == "* <" and line[-1] == ">", f"Invalid format at line {i}: {line}"
    
                entity_line = line[3:-1]
                entity_chunk = entity_line.split("|")
                assert len(entity_chunk) == 3, f"Invalid format at line {i}: {entity_line}"

                subject = process_coreference(entity_chunk[0])
                relation = [entity_chunk[1].strip()]
                object = process_coreference(entity_chunk[2])

                cluster_list.append({
                    "subject": subject,
                    "relation": relation,
                    "object": object
                })

            break # if everything is fine, break the loop
        except:
            error_counter += 1
            if error_counter > 5:
                raise RuntimeError("Too many errors. Please restart the program.")
            else:
                continue

    message_list.append({"role": "assistant", "content": gpt_response})

    return cluster_list, message_list


def process_coreference(coreference_string):
    coreferences = re.findall(r"\[.*?\]", coreference_string)
    return [x.strip() for x in coreferences[0][1:-1].split("+")] if coreferences else [coreference_string.strip()]


def get_multidoc_triples(article_list: list) -> list:
    cluster_list = []

    for each_article in article_list:
        article_triple, message_list = get_extracted_triples(each_article)
        article_cluster, message_list = get_clustered_entity(message_list)
        cluster_list.extend(article_cluster)

    # Combine the subject of each triple if they share same subject (but not stopword)
    final_cluster_list = []
    for each_cluster in cluster_list:
        combined_subject = [x.lower() for x in each_cluster['subject']]
        for another_cluster in cluster_list:
            if each_cluster != another_cluster:
                # If one of subject is in another cluster's subject
                # Lower case the subject
                another_cluster_subject = [x.lower() for x in another_cluster['subject']]

                if set(combined_subject).intersection(set(another_cluster_subject)) != set():
                    if set(combined_subject).intersection(set(another_cluster_subject)).issubset(set(stop_list)):
                        continue

                    combined_subject = combined_subject + another_cluster_subject # combine two subjects
                    combined_subject = list(set(combined_subject))

        final_cluster_list.append({
            "subject": combined_subject,
            "relation": each_cluster['relation'],
            "object": each_cluster['object']
        })

    # Combine the object of each triple if they share same object (but not stopword)
    final_cluster_list2 = []
    for each_cluster in final_cluster_list:
        combined_object = [x.lower() for x in each_cluster['object']]
        for another_cluster in final_cluster_list:
            if each_cluster != another_cluster:
                # If one of subject is in another cluster's subject
                # Lower case the subject
                another_cluster_object = [x.lower() for x in another_cluster['object']]

                if set(combined_object).intersection(set(another_cluster_object)) != set():
                    if set(combined_object).intersection(set(another_cluster_object)).issubset(set(stop_list)):
                        continue
                    combined_object = combined_object + another_cluster_object
                    combined_object = list(set(combined_object))

        final_cluster_list2.append({
            "subject": each_cluster['subject'],
            "relation": each_cluster['relation'],
            "object": combined_object
        })

    # Count the number of reference in each subject of each triple and sort them in descending order
    for each_cluster in final_cluster_list2:
        subject_count = {}
        for subject in each_cluster['subject']:
            subject_count[subject] = 0
            # Read each article and count the number of reference
            for article in article_list:
                subject_count[subject] += article.lower().count(subject)

        # Sort the cluster in descending order
        sorted_subject = sorted(subject_count.items(), key=lambda x: x[1], reverse=True)
        each_cluster['subject'] = [x[0] for x in sorted_subject]

        # Stopword will always be in the end of the list
        common_stopwords = set(each_cluster['subject']).intersection(set(stop_list))
        if common_stopwords != set():
            stopword = list(common_stopwords)[0]
            each_cluster['subject'].remove(stopword)
            each_cluster['subject'].append(stopword)
    
    # Count the number of reference in each object of each triple and sort them in descending order
    for each_cluster in final_cluster_list2:
        object_count = {}
        for object in each_cluster['object']:
            object_count[object] = 0
            # Read each article and count the number of reference
            for article in article_list:
                object_count[object] += article.lower().count(object)

        # Sort the cluster in descending order
        sorted_object = sorted(object_count.items(), key=lambda x: x[1], reverse=True)
        each_cluster['object'] = [x[0] for x in sorted_object]

        # Stopword will always be in the end of the list
        common_stopwords = set(each_cluster['object']).intersection(set(stop_list))
        if common_stopwords != set():
            stopword = list(common_stopwords)[0]
            each_cluster['object'].remove(stopword)
            each_cluster['object'].append(stopword)

    # Sort clusters by subject in alphabetical order
    final_cluster_list2 = sorted(final_cluster_list2, key=lambda x: x['subject'])

    # Create a list of unique subjects
    subject_list = []
    for each_cluster in final_cluster_list2:
        if each_cluster['subject'] not in subject_list:
            subject_list.append(each_cluster['subject'])

    # Keep only first subject and object of each triple in final_cluster_list2
    for each_cluster in final_cluster_list2:
        each_cluster['subject'] = each_cluster['subject'][0]
        each_cluster['relation'] = each_cluster['relation'][0]
        each_cluster['object'] = each_cluster['object'][0]

    return final_cluster_list2, subject_list


if __name__ == '__main__':
    
    article_list = [
        "The classic tetris world championships is one of the best gaming events to spectate all year. It's easy to understand, gets real intense, and the commentary adds a ton to the proceedings. But this year had an extra element of spice, after 16-year-old joseph saelee obliterated a seven-time world champion to become the king of tetris. The tetris championships are full of familiar faceds, with people who have been playing for aeons. Saelee, on the other hand, had to qualify for the finals. But qualify he did, coming into the final bracket as the fifth seed - not a bad effort for his first finals appearance. Saelee nearly didn't make it to the finals, having found himself on the ropes in the semi-finals against japanese grand master koryan. The intensity is fascinating, as players make split-second decisions on whether to continue building their playfield versus clearing",
        "All photos © coley brown most days, jonas neubauer wakes up a little before noon and either goes to work as a taproom manager in southern california or to his other job where he helps run a recreational marijuana startup. But today the 37-year-old los angeles native rolled out of bed a little earlier, still groggy, to talk on the phone about his other life — his most prominent and public one — as the greatest tetris player in the world. It's a title that grows more inarguable as neubauer racks up championship after championship. Eight classic tetris world championship ( ctwc ) tournaments have been held since the competition's inception in 2010. Neubauer has won seven of them. On one hand, neubauer is just a normal guy who works at a bar, drinks a lot of coffee, and plays video games in his downtime. On the other, he '",
        "Image copyright classic tetris world championship image caption joseph saelee and finalist jonas neubauer at the contest. A 16-year-old boy from california was the surprise winner of the grand final of the classic tetris world championship in oregon. The iconic block stacking computer game is 13 years older than him. Joseph saelee beat jonas neubauer, who has won seven times in the tournament's eight-year history. He told the bbc he had started playing as a hobby after watching the championships in 2016, and he plays on an original 1985 nintendo nes console. He said he practises for a couple of hours each day on the device, hooked up to a \" blocky \" cathode ray tube ( crt ) television screen rather than a modern thin screen. Mr saelee said he prefers using the old-fashioned monitor because there is less latency - a tiny time difference between the controller and the visual. \" my",
    ]

    summary, message_list = get_initial_summary(article_list)
    print("[Initial summary]:", summary)
    
    processed_cluster_list, subject_list = get_multidoc_triples(article_list)

    print("[Processed cluster list]\n", processed_cluster_list)
    print("\n\n[Subject list]\n", subject_list)
