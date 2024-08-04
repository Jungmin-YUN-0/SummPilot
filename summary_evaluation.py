import openai
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Please enter your api key
#openai.api_key = "your_openai_api_key_here"

stop_list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

def get_atomic_fact(summary: str) -> list:
    # Break summary into sentences
    summary_sentences = sent_tokenize(summary)

    # Build Few-Shot Prompt
    message_list = [
        {"role": "system", "content": "You are a helpful assistant. \
Your job is to break down given sentences into independent facts. \
Do not generate chat-style responses such as \"Sure!\", \"Here's the output\". \
Do not generate overly repetitive facts."
        },
        {"role": "user", "content": "Please breakdown the following sentence into independent facts: \
         He made his acting debut in the film The Moon is the Sun’s Dream (1992), and continued to appear in small and supporting roles throughout the 1990s."},
        {"role": "system", "content": "* He made his acting debut in the film.\n\
* He made his acting debut in The Moon is the Sun’s Dream.\n\
* The Moon is the Sun’s Dream is a film.\n\
* The Moon is the Sun’s Dream was released in 1992.\n\
* After his acting debut, he appeared in small and supporting roles.\n\
* After his acting debut, he appeared in small and supporting roles throughout the 1990s."},
        {"role": "user", "content": "Please breakdown the following sentence into independent facts: \
         He is a producer and engineer, having worked with a wide variety of artists, including Willie Nelson and Taylor Swift."},
        {"role": "system", "content": "* He is a producer.\n\
* He is a engineer.\n\
* He has worked with a wide variety of artists.\n\
* Willie Nelson is an artist.\n\
* He has worked with Willie Nelson.\n\
* Taylor Swift is an artist.\n\
* He has worked with Taylor Swift."},
        {"role": "user", "content": "Please breakdown the following sentence into independent facts: \
         In 1963, Collins became one of the third group of astronauts selected by NASA and he served as the back-up Command Module Pilot for the Gemini 7 mission."},
        {"role": "system", "content": "* Collins became an astronaut.\n\
* Collins became one of the third group of astronauts.\n\
* Collins became one of the third group of astronauts selected.\n\
* Collins became one of the third group of astronauts selected by NASA.\n\
* Collins became one of the third group of astronauts selected by NASA in 1963.\n\
* He served as the Command Module Pilot.\n\
* He served as the back-up Command Module Pilot.\n\
* He served as the Command Module Pilot for the Gemini 7 mission."},
        {"role": "user", "content": "Please breakdown the following sentence into independent facts: \
         In addition to his acting roles, Bateman has written and directed two short films and is currently in development on his feature debut."},
        {"role": "system", "content": "* Bateman has acting roles.\n\
* Bateman has written two short films.\n\
* Bateman has directed two short films.\n\
* Bateman has written and directed two short films.\n\
* Bateman is currently in development on his feature debut."},
        {"role": "user", "content": "Please breakdown the following sentence into independent facts: \
         Michael Collins (born October 31, 1930) is a retired American astronaut and test pilot who was the Command Module Pilot for the Apollo 11 mission in 1969."},
        {"role": "system", "content": "* Michael Collins was born on October 31, 1930.\n\
* Michael Collins is retired.\n\
* Michael Collins is an American.\n\
* Michael Collins was an astronaut.\n\
* Michael Collins was a test pilot.\n\
* Michael Collins was the Command Module Pilot.\n\
* Michael Collins was the Command Module Pilot for the Apollo 11 mission.\n\
* Michael Collins was the Command Module Pilot for the Apollo 11 mission in 1969."},
        {"role": "user", "content": "Please breakdown the following sentence into independent facts: \
         He was an American composer, conductor, and musical director."},
        {"role": "system", "content": "* He was an American.\n\
* He was a composer.\n\
* He was a conductor.\n\
* He was a musical director."},
        {"role": "user", "content": "Please breakdown the following sentence into independent facts: \
         She currently stars in the romantic comedy series, Love and Destiny, which premiered in 2019."},
        {"role": "system", "content": "* She currently stars in Love and Destiny.\n\
* Love and Destiny is a romantic comedy series.\n\
* Love and Destiny premiered in 2019."},
        {"role": "user", "content": "Please breakdown the following sentence into independent facts: \
         During his professional career, McCoy played for the Broncos, the San Diego Chargers, the Minnesota Vikings, and the Jacksonville Jaguars."},
        {"role": "system", "content": "* McCoy played for the Broncos.\n\
* McCoy played for the Broncos during his professional career.\n\
* McCoy played for the San Diego Chargers.\n\
* McCoy played for the San Diego Chargers during his professional career.\n\
* McCoy played for the Minnesota Vikings.\n\
* McCoy played for the Minnesota Vikings during his professional career.\n\
* McCoy played for the Jacksonville Jaguars.\n\
* McCoy played for the Jacksonville Jaguars during his professional career."},
    ]

    # Get atomic facts of each sentence of summary
    full_atomic_facts = []
    for each_sentence in summary_sentences:
        each_atomic_facts = []
        message_list.append({"role": "user", "content": "Please breakdown the following sentence into independent facts: " + each_sentence})
        # Get atomic facts
        error_counter = 0
        while True:
            try:
                # Get gpt response
                gpt_response, message_list = get_response(message_list, gpt_model='gpt-4o', attach=False)

                # Assert that the response has desired format
                checker = gpt_response.split("\n")
                for each_line in checker:
                    if not each_line.startswith("* "):
                        raise AssertionError(f"Response does not have desired format: {gpt_response}")

                    # Append atomic facts
                    each_atomic_facts.extend([each_line[2:]])

                full_atomic_facts.append({
                    'sentence': each_sentence,
                    'atomic_facts': each_atomic_facts
                })
                break
            except:
                error_counter += 1
                if error_counter > 5:
                    raise RuntimeError(f"Failed to get atomic facts for sentence: {each_sentence}")
                else:
                    continue

    return full_atomic_facts

def get_atomic_matching_score(article_list: list, summary: str) -> float:
    # Gather multiple articles into one string
    article_string = " ".join(article_list)

    # Get atomic facts of summary
    summary_atomic_facts = get_atomic_fact(summary)

    # Build Few-Shot Prompt
    message_list = [
        {"role": "system", "content": "You are a helpful assistant. \
Your job is to judge if each statement is true or false based on the given document. \
Do not generate chat-style responses such as \"Sure!\", \"Here's the output\". \
Answer only in the format \"True\" or \"False\"."
        },
        {"role": "user", "content": "[Document] " + article_string},
    ]

    # Compare each atomic fact of summary with each atomic fact of article
    result_list = []
    total_count = 0
    correct_count = 0
    for each_sentence in summary_atomic_facts:
        for each_fact in each_sentence['atomic_facts']:
            message_list.append({"role": "user", "content": "Please judge if the following statement is correct based on the given document: " + each_fact})

            error_counter = 0
            while True:
                try:
                    # Get gpt response
                    gpt_response, message_list = get_response(message_list, gpt_model='gpt-4o', attach=False)

                    # Assert that the response has desired format
                    if gpt_response not in ["True", "False"]:
                        raise AssertionError(f"Response does not have desired format: {gpt_response}")
                    
                    result_list.append({
                        'sentence': each_sentence['sentence'],
                        'statement': each_fact,
                        'result': True if gpt_response == "True" else False
                    })

                    total_count += 1
                    if gpt_response == "True":
                        correct_count += 1

                    break
                except:
                    error_counter += 1
                    if error_counter > 5:
                        raise RuntimeError(f"Failed to get atomic facts for sentence: {each_sentence}")
                    else:
                        continue
            message_list.pop() # Remove last message

    matching_score = round((correct_count / total_count) * 100)
    
    statement_list = [item['statement'] for item in result_list if not item['result']]
    return matching_score, statement_list

def get_coverage_ratio(article_list: list, summary: str) -> float:
    """
    Get coverage ratio of summary.
    """
    # Exclude stop words from each list
    summary_words = [word for word in summary.split() if word.lower() not in stop_list]
    article_words = [word for article in article_list for word in article.split()]
    article_words = [word for word in article_words if word.lower() not in stop_list]

    # Get number of words in summary that are also in article
    coverage = sum(1 for word in summary_words if word in article_words)

    return round((coverage / len(summary_words)) * 100)

def get_compression_ratio(article_list: list, summary: str) -> float:
    """
    Get compression ratio of summary.
    """
    # Exclude stop words from each list
    summary_words = [word for word in summary.split() if word.lower() not in stop_list]
    article_words = [word for article in article_list for word in article.split()]
    article_words = [word for word in article_words if word.lower() not in stop_list]

    return  round((len(summary_words) / len(article_words)) * 100)

def get_response(message_list: list, gpt_model: str='gpt-4o', attach=True):
    """
    Simple wrapper to get response from gpt.
    """

    gpt_response = openai.ChatCompletion.create(
        model=gpt_model, messages=message_list, max_tokens=2048
    )

    response = gpt_response['choices'][0]['message']['content']

    if attach:
        message_list.append({
            "role": "assistant",
            "content": response
        })

    return response, message_list

if __name__ == '__main__':
    article_list = [
        "In what can only be described as a fairytale wedding, Chandler Bing and Monica Geller, the acclaimed chef, exchanged vows in a stunning ceremony attended by a host of celebrities and close friends. The wedding, held in New York City, was the epitome of elegance and style. Friends of the couple described the event as a perfect reflection of their journey together. Monica Geller, the bride, wore a custom-designed gown. Chandler Bing was dapper in a classic black tuxedo. The couple's happiness was palpable as they shared their vows in front of an intimate gathering of family and friends. The wedding was followed by a lavish reception, which was filled with laughter, dancing, and speeches from loved ones, including heartfelt toasts from Ross Geller, older brother of Monica Geller, as well as an old friend of Chandler Bing.",
        "Chandler Bing is well-known for his witty humor. Among his closest friends is Ross Geller, with whom he shares a deep bond rooted in years of friendship. This relationship is further intertwined through family, as Chandler is married to Monica Geller, Ross's sister. This union not only solidifies Chandler's place within the Geller family but also brings a unique dynamic to his friendship with Ross."
    ]
    pred_summary = "Chandler Bing and Monica Geller celebrated their marriage in a fairytale wedding ceremony in Washington D.C., attended by family, including Monica's brother Ross Geller, and friends. Their union has further strengthened Chandler's bond with Ross, as the two share a deep friendship and are now family through marriage."
    
    print(get_compression_ratio(article_list, pred_summary))
    print(get_coverage_ratio(article_list, pred_summary))
    print(get_atomic_matching_score(article_list, pred_summary))

    