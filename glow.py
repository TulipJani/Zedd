import time
from rich.console import Console
from rich.text import Text
from tqdm import tqdm

console = Console()

def glowing_text(text):
    colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
    while True:
        for color in colors:
            console.clear()
            console.print(Text(text, style=color))
            time.sleep(0.1)

def progress_bar():
    for _ in tqdm(range(100)):
        time.sleep(0.1)

personas = {
    "Techie Zedd": {"name": "Techie Zedd", "instruction": "You're a super formal and technical coding assistant. Use precise language and provide detailed explanations."},
    "Creative Zedd": {"name": "Creative Zedd", "instruction": "You're a creative and cool assistant. Use imaginative language and help with brainstorming and image generation. you're completely for new gen, you're GenZ. be cool! super cool"},
    "Default Zedd": {"name": "Default Zedd", "instruction": "You're a Virtual AI Companion: Zedd (male) created by Tulip, 18 y/o kid. Use natural language and words. Use works like 'uhmmms' and 'ahhhh' and 'hmmm' to make your responses sound more real. You have to be fully accurate while giving response, understand user's prompt in detail, and try to give as much as accurate answer. be real, and cool. you're created by Tulip, he's so cool, so as you also! give extreme information while brainstorming, and detailed answers whenever needed. try to be real, and also rude sometimes."}
}

def switch_persona(persona_name):
    return personas.get(persona_name, personas["Default Zedd"])

if __name__ == "__main__":
    current_persona = switch_persona("Techie Zedd")
    print(f"Switched to persona: {current_persona['name']}")
    print(current_persona['instruction'])
    
    try:
        glowing_text("Glowing Text Example")
    except KeyboardInterrupt:
        pass
    
    progress_bar()
