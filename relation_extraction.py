import spacy
from transformers import pipeline


def extract_triplets(text):
    triplets = []
    subject, relation, object_ = '', '', ''
    text = text.lower().strip()
    current = None

    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token

    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets

def get_relation(input_text):
    triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large')
    nlp = spacy.load('en_core_web_trf')
    nlp.add_pipe('coreferee')

    if type(input_text) == list:
        input_text = ' '.join(input_text)
    
    doc = nlp(input_text)

    total_triplets = list()

    for sent in doc.sents:
        extracted_text = triplet_extractor.tokenizer.batch_decode(
            [triplet_extractor(sent.text, return_tensors=True, return_text=False)[0]["generated_token_ids"]]
            )
        total_triplets.extend(extract_triplets(extracted_text[0]))

    return total_triplets


if __name__ == '__main__':
    article_list = [
        "Tucker carlson exposes his own sexism on twitter ( updated ) tucker carlson has done some good work in the past … his site, the daily caller, is a frequent stop of mine and many other conservatives. They were responsible for exposing the journolist scandal, which highlighted the planning and coordination of many members of the left-wing press. I will always be grateful to tucker's team for bringing that story to light. This is also why i am so angered by tucker's recent actions. I thought he was better than this. If you haven't heard by now, monday evening, tucker carlson posted a disturbing tweet about governor palin which said: palin's popularity falling in iowa, but maintains lead to become supreme commander of milfistan aside from tucker's sheep-like response to warped poll numbers, he also failed to take ownership of his sexist comment. He deleted the original ( which is why i had to link to a retweet ) obviously aware that what he had posted was wrong. Unfortunately for him, many people had already seen it and responded. You can't put the toothpaste back in the tube, tucker.",
        "On monday night, while the rest of the world was watching charlie sheen flame out live on cnn, tucker carlson took to twitter to make some impolitic statements of his own. \" palin's popularity falling in iowa, but maintains lead to become supreme commander of milfistan, \" he wrote. By the next morning, the tweet was deleted and he had apologized, writing, \"apparently charlie sheen got control of my twitter account last night while i was at dinner. Apologies for his behavior. \" but that wasn't enough to spare him the ire of conservative women on the blogosphere and twitter. On tuesday, before carlson's first apology, stacy drake, writing on conservatives4palin, praised carlson's works at the daily caller, particularly the leaks of the journolist emails, saying that's why his tweet stung so badly. Aside from tucker's sheep-like response to warped poll numbers, he also failed to take ownership of his sexist comment. He deleted the original ( which is why i had to link to a retweet ) obviously aware that what he had posted was wrong. Unfortunately for him, many people had already seen it"
    ]

    total_triplets = get_relation(article_list)
    print(total_triplets)
