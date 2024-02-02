from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai


app = Flask(__name__)
CORS(app)

api_key = "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"
openai.api_key = api_key

def analyze_review(review_text):
    
    parameters = {
        'model':"gpt-3.5-turbo",
        'messages':[],
        'max_tokens':"200",
        'n':"1",
        'stop':"None",
        'temperature':"0.7"
    }
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content":"You are an AI assistant"},
                  {"role": "user", "content":"{review}Given a set of reviews for a product, please identify the product, and for each of the specified attributes, extract the positives and negatives mentioned in the reviews. The format should be as follows:Product Name: [Name of the Product] \n Attributes: [attribute name]:\nPositive: [Positive aspects related to Attribute ]\nNegative: [Negative aspects related to Attribute ] and continue for few attributes in next line Attributes: [attribute name]:Positive: [Positive aspects related to Attribute ] Negative: [Negative aspects related to Attribute ] count Attributes: [attribute name]:Positive: [Positive aspects related to Attribute ] Negative: [Negative aspects related to Attribute ] count Attributes: [attribute name]:Positive: [Positive aspects related to Attribute ] Negative: [Negative aspects related to Attribute ] count .Please ensure that the extracted information follows this format.Do not repeat the attributes.also provide the count of the positives and negatives under each attribute.print each in next line"
                   "Amazing sound quality.Good battery life.Fits well"
                    "Fast connection fast charging best sound quality best long time battery this price valuable Airdopes"
                    "Sound quality is good.Fast charging.Easy to use.Value for money"
                    "Right side of the earphone is not working.... Got defective piece of earphones.... some parts are broken... Really disappointing.."
                    "the earphone is very heavy and charging is slow.The sound quality is the best aspect of the Noise Bluetooth Earbuds. The sound of music and videos is clear and balanced. The bass is good, but not too much. The highs are clear and without any distortion."
                    "the earphone doesnt fit good, it always falls from ear.It hurts my ear after sometime"
                    "the earphones take so much time to connect to the device. Charging is fast. It looks nice"
                    "Battery and sound is too good.The microphone quality is very poor. When you make a phone call, the other person can hear you, but they can hear you in very poor quality. The microphone has a lot of noise, and the voice cannot be heard clearly."
                    "The product is stylish and look good, battery back is good connecting device is also good but the sound quality is not good for those who want bass and calling sound is very bad."
                    "The product is good nd the sound quality also good the charge also working for a long time I'm impressed by the noise product."
                    "Audio quality is very good, battery backup is almost 50 hours with case, designer super cool, comfortable with ears , compatible to carry everywhere."
                    "Having Low voice during Calls and meeting, rest ots sound is very nice with very low buffer and noise issue with good connectivity."
                    "Only thing disappointed me is , its low our voice to caller"
                    "Amazing Sound quality.Fantastic look.Great power backup.Totally worth"
                    "The sound quality is really good, charges really fast, touch is good as well.  easy to carry and superfast charging!And I love how it connects so easily and quickly. I would recommend to buy this, worth the price!!."}],
        max_tokens=200
        
    )

    reply = response.choices[0].message.content
    return reply

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_text", methods=["POST"])
def generate_text():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"})

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"})

        file_content = file.read().decode('utf-8')
        positive_text = analyze_review(file_content)

        return jsonify({"generated_text": positive_text})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
