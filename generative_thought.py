# 45.79.67.135
# 
# Example call:
# r = requests.post("http://45.79.67.135/gpt3", json={'query':['free will']})
#
# To run:
# cd /home/utmist-omni
# gunicorn3 generative_thought:app
#
# To restart & run contiually:
# lsof -ti tcp:8000 | xargs kill -9
# tmux kill-session -t prod
# tmux new-session -s prod -d “gunicorn3 generative_thought:app”

# Imports
from flask import Flask, request, render_template, url_for, copy_current_request_context, redirect, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_cors import CORS
import logging
import openai
import os
from dotenv import load_dotenv

# Initializations
app = Flask(__name__)
api = Api(app)
CORS(app, resources={"/gpt3": {"origins": "*"},}, supports_credentials=True)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Generate Contradiction
class GenerateContradiction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('claim', type=str)
        
    def generate_contradiction(claim):
        prompt = """'%s'
        An ingenous expert wrote a detailed counterargument to this claim, saying:
        """%(claim)
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=prompt,
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        text = response['choices'][0]['text']
        return text
      
    def get(self):
        args = self.parser.parse_args()
        claim = args['claim']
        return self.generate_contradiction(claim)
    
    def post(self):
        args = self.parser.parse_args()
        claim = args['claim']
        return self.generate_contradiction(claim)
        
api.add_resource(GenerateContradiction, "/contradiction")

# Generate Enhancement
class GenerateEnhancement(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('prefix', type=str)
    
    def generate_enhancement(prefix):
        prompt_text = 'Prompt:  "a group of esoteric cult members in the desert\nEnhancement:  by Cinestill 800t trending on Flickr wear red tunics and gold mask and jewels" \nPrompt:  star trek character wearing red smoking and fighting a giant space beetle\nEnhancement:  4k   \nPrompt:  "star trek character wearing red smoking and fighting a giant space beetle\nEnhancement:  4k" \nPrompt:  Octahedron made of salami on a dinner plate\nEnhancement:  Michelin Star presentation \nPrompt:  Saul Goodman in Star Trek the next generation\nEnhancement:  tv still 4k \nPrompt:  "Octahedron made of salami on a dinner plate\nEnhancement:  Michelin Star presentation" \nPrompt:  "Saul Goodman in Star Trek the next generation\nEnhancement:  tv still 4k" \nPrompt:  Detailed anime key visual of Monika\nEnhancement:  from Doki Doki Literature Club wearing a white dress at Santa Monica Pier\nPrompt:  "Detailed anime key visual of Monika\nEnhancement:  from Doki Doki Literature Club wearing a white dress at Santa Monica Pier" \nPrompt:  saul goodman dressed as a star trek character\nEnhancement:  tv still 4k \nPrompt:  "the vast landscape of a alien planet in the HD1 galaxy\nEnhancement:  well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting" \nPrompt:  scary horror creature\nEnhancement:  well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting \nPrompt:  "scary horror creature\nEnhancement:  well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting" \nPrompt:  a messy bedroom with several tall mirrors\nEnhancement:  well lit studio photo \nPrompt:  art by aleksander rostov\nEnhancement:  disco elysium \nPrompt:  "a messy bedroom with several tall mirrors\nEnhancement:  well lit studio photo" \nPrompt:  "art by aleksander rostov\nEnhancement:  disco elysium" \nPrompt:  scary horror creature\nEnhancement:  well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting painted by Zdzisław Beksiński \nPrompt:  "scary horror creature\nEnhancement:  well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting painted by Zdzisław Beksiński" \nPrompt:  Mountain of floppy disks\nEnhancement:  award winning photo by Edward Burtynsky \nPrompt:  "8k pov of a tribe in the desert\nEnhancement:  Cinestill 800t cinematic trending on Flickr wear red tunics and gold mask and jewels" \nPrompt:  Yoda with an ak47\nEnhancement:  looking threatening well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting \nPrompt:  "Mountain of floppy disks\nEnhancement:  award winning photo by Edward Burtynsky" \nPrompt:  "8k pov of a tribe in the desert\nEnhancement:  Cinestill 800t cinematic trending on Flickr wear red tunics and gold mask and jewels" \nPrompt:  "Yoda with an ak47\nEnhancement:  looking threatening well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting" \nPrompt:  "a group of esoteric cult members in the desert\nEnhancement:  by Cinestill 800t trending on Flickr wear red tunics and a golden mask and jewels" \nPrompt:  cyberpunk grand piano\nEnhancement:  RGB colored \nPrompt:  "a group of esoteric cult members in the desert\nEnhancement:  by Cinestill 800t trending on Flickr wear red tunics and a golden mask and jewels" \nPrompt:  Will smith holding a toy gun with a slapper hand on it pointing it at Chris rock\nEnhancement:  well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting \nPrompt:  "cyberpunk grand piano\nEnhancement:  RGB colored" \nPrompt:  "vintage photo group portrait of a esoteric cult members in desert\nEnhancement:  early black and white 8mm wear red tunics and gold mask and jewels" \nPrompt:  "Will smith holding a toy gun with a slapper hand on it pointing it at Chris rock\nEnhancement:  well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting" \nPrompt:  "vintage photo group portrait of a esoteric cult members in desert\nEnhancement:  early black and white 8mm wear red tunics and gold mask and jewels" \nPrompt:  coffee latte art of a Mandelbrot fractal\nEnhancement:  flickr trending \nPrompt:  "coffee latte art of a Mandelbrot fractal\nEnhancement:  flickr trending" \nPrompt:  3d render of Mario as a cyborg\nEnhancement:  4k uhd ray trace \nPrompt:  "coffee latte art of a Mandelbrot fractal\nEnhancement:  flickr trending" \nPrompt:  "3d render of Mario as a cyborg\nEnhancement:  4k uhd ray trace" \nPrompt:  "vintage photo group portrait of a esoteric cult members in desert\nEnhancement:  early black and white 8mm wear red tunics and gold mask and jewels" \nPrompt:  "coffee latte art of a Mandelbrot fractal\nEnhancement:  flickr trending" \nPrompt:  a painting of a giant bird destroying New York City\nEnhancement:  Time Square giant destruction everywhere fires explosions disaster well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting \nPrompt:  artificial intelligence\nEnhancement:  art by aleksander rostov disco elysium \nPrompt:  "photo group portrait of members of esoteric cult in front of a mystic temple\nEnhancement:  ektachrome wear red tunics and gold mask and jewels" \nPrompt:  "artificial intelligence\nEnhancement:  art by aleksander rostov disco elysium" \nPrompt:  wine glass full of marbles\nEnhancement:  standing on a coffee table 4K studio photo \nPrompt:  "photo group portrait of members of esoteric cult in front of a mystic temple\nEnhancement:  ektachrome wear red tunics and mask made of gold and jewels" \nPrompt:  "wine glass full of marbles\nEnhancement:  standing on a coffee table 4K studio photo" \nPrompt:  a painting of a giant bird destroying New York City\nEnhancement:  Time Square giant destruction everywhere fires explosions disaster well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting \nPrompt:  "a painting of a giant bird destroying New York City\nEnhancement:  Time Square giant destruction everywhere fires explosions disaster well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting" \nPrompt:  marbles in a wine glass\nEnhancement:  standing on a coffee table 4K studio photo \nPrompt:  "goddess portrait. jellyfish butterfly phoenix head. intricate artwork by Tooth Wu and wlop and beeple and dan mumford. octane render\nEnhancement:  trending on artstation greg rutkowski very coherent symmetrical artwork. cinematic hyper realism high detail octane render 8k depth of field bokeh" \nPrompt:  "marbles in a wine glass\nEnhancement:  standing on a coffee table 4K studio photo" \nPrompt:  a painting of a giant bird destroying New York City\nEnhancement:  Time Square giant destruction everywhere fires explosions disaster well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting \nPrompt:  "a painting of a giant bird destroying New York City\nEnhancement:  Time Square giant destruction everywhere fires explosions disaster well lit digital art virtuosic painting award winning high quality visual sharp backlit gorgeous lighting" \nPrompt:  blonde wife undressing\nEnhancement:  painting by Vladimir Volegov \nPrompt:  "blonde wife undressing\nEnhancement:  painting by Vladimir Volegov" \nPrompt:  "photo group portrait of members of esoteric cult in front of a mystic temple\nEnhancement:  ektachrome wear red tunics and mask made of gold and jewels" \nPrompt:  "goddess portrait. jellyfish butterfly phoenix head. intricate artwork by Tooth Wu and wlop and beeple and dan mumford. octane render\nEnhancement:  trending on artstation greg rutkowski very coherent symmetrical artwork. cinematic hyper realism high detail octane render 8k depth of field bokeh" \nPrompt:  painting of giant evil looking demon bird destroying New York City\nEnhancement:  Time Square giant destruction everywhere fires explosions well lit masterpiece virtuosic painting high quality visual sharp backlit gorgeous lighting \nPrompt:  "yper realistic and detailed photo group portrait of members of esoteric cult in front of red pyramids\nEnhancement:  restored ektachrome vivid color wear red tunics and gold mask and jewels" \nPrompt:  "painting of giant evil looking demon bird destroying New York City\nEnhancement:  Time Square giant destruction everywhere fires explosions well lit masterpiece virtuosic painting high quality visual sharp backlit gorgeous lighting" \nPrompt:  Times Square flooded with crystal clear water on a sunny day\nEnhancement:  4K photo \nPrompt:  blonde wife in her underwear making breakfast\nEnhancement:  impressionism painting \nPrompt:  "hyper realistic and detailed photo group portrait of members of esoteric cult in front of red pyramids\nEnhancement:  restored ektachrome vivid color wear red tunics and gold mask and jewels" \nPrompt:  "Times Square flooded with crystal clear water on a sunny day\nEnhancement:  4K photo" \nPrompt:  face portrait avantgarde fashion spinal biomechanical exoskeleton armor helmet masked people from future tokyo fashion photography\nEnhancement:  artistic photography beautiful hypebeast 8K intricate detailed fashion promo  \nPrompt:  "hyper realistic and detailed photo group portrait of members of esoteric cult in front of red pyramids\nEnhancement:  restored ektachrome vivid color wear red tunics and gold mask and jewels" \nPrompt:  Heath Ledger smoking a cigarette back alley of prom\nEnhancement:  well lit masterpiece virtuosic painting high quality visual sharp backlit gorgeous lighting \nPrompt:  Spaceship graveyard\nEnhancement:  award winning 4K photo by Edward Burtynsky \nPrompt:  a hyperrealistic 3d steampunk rubix cube in the palm of a robot\'s hand\nEnhancement:  4k highly detailed \nPrompt:  spider spirit spider dreams\nEnhancement:  red and black white spider web ghost smoke\nPrompt:  "Heath Ledger smoking a cigarette back alley of prom\nEnhancement:  well lit masterpiece virtuosic painting high quality visual sharp backlit gorgeous lighting" \nPrompt:  "Spaceship graveyard\nEnhancement:  award winning 4K photo by Edward Burtynsky" \nPrompt:  "a hyperrealistic 3d steampunk rubix cube in the palm of a robot\'s hand\nEnhancement:  4k highly detailed" \nPrompt:  "face portrait avantgarde fashion spinal biomechanical exoskeleton armor helmet masked people from future tokyo fashion photography\nEnhancement:  artistic photography beautiful hypebeast 8K intricate detailed fashion promo" \nPrompt:  "spider spirit spider dreams\nEnhancement:  red and black white spider web ghost smoke" \nPrompt:  "Heath Ledger smoking a cigarette back alley of prom\nEnhancement:  well lit masterpiece virtuosic painting high quality visual sharp backlit gorgeous lighting" \nPrompt:  A chair inspired by spaghetti\nEnhancement:  product photography \nPrompt:  meteor mining facility\nEnhancement:  award winning 4K photo by Edward Burtynsky \nPrompt:  "A chair inspired by spaghetti\nEnhancement:  product photography" \nPrompt:  face portrait spinal biomechanical matte black exoskeleton armor masked people from future tokyo fashion photography\nEnhancement:  artistic photography beautiful hypebeast 8K intricate detailed fashion promo \nPrompt:  a jinn lurking behind a muslim\nEnhancement:  digital art realistic unreal engine 4\nPrompt:  "meteor mining facility\nEnhancement:  award winning 4K photo by Edward Burtynsky" \nPrompt:  "a jinn lurking behind a muslim\nEnhancement:  digital art realistic unreal engine 4" \nPrompt:  professional photo of a kitten playing with a ball of yarn\nEnhancement:  4k highly detailed \nPrompt:  "professional photo of a kitten playing with a ball of yarn\nEnhancement:  4k highly detailed" \nPrompt:  "Heath Ledger smoking a cigarette back alley of prom\nEnhancement:  well lit masterpiece virtuosic painting high quality visual sharp backlit gorgeous lighting" \nPrompt:  "Heath Ledger smoking a cigarette back alley of prom\nEnhancement:  well lit masterpiece photography high quality visual sharp backlit gorgeous lighting" \nPrompt:  black and red\nEnhancement:  Computer case made of Red welded rods with glass sides and a green motherboard\nPrompt:  "black and red\nEnhancement:  Computer case made of Red welded rods with glass sides and a green motherboard" \nPrompt:  A stormy rainy sky with black puffy clouds and a beautiful twisting rainbow\nEnhancement:  Huge heavy rain slants across the scene matte painting \nPrompt:  "woman\nEnhancement:  magical flower bright castleton green detailed intricate ink illustration dark atmosphere detailed illustration hd 4k digital art overdetailed art concept art complementing colors trending on artstation Cgstudio the most beautiful image ever created dramatic subtle details by alphonse mucha" \nPrompt:  "woman\nEnhancement:  magical flower bright castleton green detailed intricate ink illustration dark atmosphere detailed illustration hd 4k digital art overdetailed art concept art complementing colors trending on artstation Cgstudio the most beautiful image ever created dramatic subtle details by alphonse mucha" \nPrompt:  The resurrected glorious dead walk in the Monongahela National Forest\nEnhancement:  by Emmanuel Lubeski anamorphic lens 4k \nPrompt:  "Heath Ledger smoking a cigarette back alley of prom\nEnhancement:  well lit masterpiece photography high quality visual sharp backlit gorgeous lighting" \nPrompt:  A stormy rainy sky with black puffy clouds and a beautiful twisting rainbow\nEnhancement:  Huge heavy rain slants across the scene matte painting \nPrompt:  "The resurrected glorious dead walk in the Monongahela National Forest\nEnhancement:  by Emmanuel Lubeski anamorphic lens 4k" \nPrompt:  face portrait avantgarde fashion spinal exoskeleton armor people from future tokyo fashion photography\nEnhancement:  artistic photography beautiful hypebeast 8K intricate detailed fashion promo \nPrompt:  "face portrait spinal biomechanical matte black exoskeleton armor masked people from future tokyo fashion photography\nEnhancement:  artistic photography beautiful hypebeast 8K intricate detailed fashion promo" \nPrompt:  "A stormy rainy sky with black puffy clouds and a beautiful twisting rainbow\nEnhancement:  Huge heavy rain slants across the scene matte painting" \nPrompt: '

        prompt = """%s + %s + '\nEnhancement: '"""%(prompt_text, prefix)

        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=prompt,
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
            stop=['\n'],
          presence_penalty=0
        )

        text = response['choices'][0]['text']
        return text

    def get(self):
        args = self.parser.parse_args()
        prefix = args['prefix']
        return self.generate_enhancement(prefix)
    
    def post(self):
        args = self.parser.parse_args()
        prefix = args['prefix']
        return self.generate_enhancement(prefix)     

api.add_resource(GenerateEnhancement, "/enhance")

# Generate Assumptiong Questioning
class GenerateAssumptionQuestioning(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('claim', type=str)
        
    def generate_assumptiong_questioning(claim):
        prompt = """'%s'
        An ingenous expert questioned the assumptions made saying:
        """%(claim)
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=prompt,
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        text = response['choices'][0]['text']
        return text
      
    def get(self):
        args = self.parser.parse_args()
        claim = args['claim']
        return self.generate_assumptiong_questioning(claim)
    
    def post(self):
        args = self.parser.parse_args()
        claim = args['claim']
        return self.generate_assumptiong_questioning(claim)
        
api.add_resource(GenerateAssumptionQuestioning, "/assumptiong-questioning")

# Generate Supporting Example
class GenerateSupportingExample(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('claim', type=str)
        
    def generate_supporting_example(claim):
        prompt = """'%s'
        A true story supporting this claim is:
        """%(claim)
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=prompt,
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        text = response['choices'][0]['text']
        return text
      
    def get(self):
        args = self.parser.parse_args()
        claim = args['claim']
        return self.generate_supporting_example(claim)
    
    def post(self):
        args = self.parser.parse_args()
        claim = args['claim']
        return self.generate_supporting_example(claim)
        
api.add_resource(GenerateSupportingExample, "/supporting-example")

# Generate Contradicting Example
class GenerateContradictingExample(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('claim', type=str)
        
    def generate_contradicting_example(claim):
        prompt = """'%s'
        A true story contradicting this claim is:
        """%(claim)
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=prompt,
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        text = response['choices'][0]['text']
        return text
      
    def get(self):
        args = self.parser.parse_args()
        claim = args['claim']
        return self.generate_contradicting_example(claim)
    
    def post(self):
        args = self.parser.parse_args()
        claim = args['claim']
        return self.generate_contradicting_example(claim)
        
api.add_resource(GenerateContradictingExample, "/contradicting-example")