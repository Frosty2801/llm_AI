from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv


load_dotenv()

def generate_pet_name(animal_type):
    llm = OpenAI(temperature=0.8)

    promp_template_name = PromptTemplate(
        input_variables=["animal_type"],
        template="Dame 5 nombres para un {animal_type} y dime por que te gustan"
    )
    
    name_chain = LLMChain(llm=llm, prompt=promp_template_name)

    response = name_chain.run({'animal_type': animal_type})
    return response



if __name__ == "__main__":
    print(generate_pet_name("perro"))

