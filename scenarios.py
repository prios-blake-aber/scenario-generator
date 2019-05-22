#!/usr/bin/env python
# coding: utf-8

# In[1]:


import enum
import typing
import random
import pandas as pd
from dataclasses import dataclass


# #### Set random seed for deterministic data generation

# In[2]:


random.seed(42)


# #### Constants

# In[3]:


RATIO_OF_RANKINGS_TO_DOTS = 0.1
LIKELIHOOD_OF_BEING_WRONG = 0.15


# In[4]:


ATTRIBUTES = {
    'Analytical Thinking': 1, 
    'Assertive and Open-Minded': 2,
    'Cuts Through It': 3,
    'Designing the Movie Script': 4, 
    'Determination': 5,
    'Empathy':6, 
    'Fighting to get in Synch': 7,
    'Linear Thinking': 8, 
    'Listens Well': 9,
    'Maintaining High Standards': 10,
    'Manages Conflict to get at Truth': 11,
    'Motivating Others': 12,
    'Perceiving Problems': 13, 
    'Precise and Meticulous Problem Solving': 14, 
    'Principled and Higher Level Thinking': 15, 
    'Pushing through to Results': 16,
    'Sizing People up': 17, 
    'Synthesizing the Situation': 18,
    'Thinking Strategically': 19, 
    'Willing to Touch the Nerve': 20
}


# In[5]:


PEOPLE_IDS = {
    'Will Haffner': '1', 
    'Alex Chavez': '2',
    'Sophia Porrino': '3',
    'Chintan Mehta': '4', 
    'Vin Marshall': '5'
}


# #### Expected Behaviors

# In[6]:


def get_random_negative_value():
    return random.randint(2, 4)

def get_random_positive_value():
    return random.randint(7, 9)

def get_observation_type(random_value, ranking_to_dot_ratio=RATIO_OF_RANKINGS_TO_DOTS):
    if random_value <= ranking_to_dot_ratio:
        return 'Ranking'
    else:
        return 'Dot'


# In[7]:


@dataclass
class Person:
    '''A Person in the PriOS Ecosystem that generates data'''
    id: str
    name: str
    description: str
    dot_factor: float
    ranking_factor: float
    weaknesses: typing.List[int]
    strengths: typing.List[int]
    likelihood_of_being_wrong: float = LIKELIHOOD_OF_BEING_WRONG
        
    def has_a_view_on(
        self, 
        other: 'Person'
    ) -> typing.List[dict]:

        random_value = random.random()
        observation_type = get_observation_type(random_value)

        return {
            'random_value': random_value,
            'author': self.id,
            'subject': other.id,
            'observation_type': observation_type,
            'attribute': None,
            'value': None,
        }

    def has_a_negative_view_on(
        self, 
        other: 'Person'
    ) -> typing.List[dict]:

        view_of_person = self.has_a_view_on(other)
        view_of_person['value'] = get_random_negative_value()

        if view_of_person['random_value'] <= self.likelihood_of_being_wrong:
            view_of_person['attribute'] = random.choice(other.strengths)
        else:
            view_of_person['attribute'] = random.choice(other.weaknesses)

        return view_of_person

    def has_a_positive_view_on(
        self, 
        other: 'Person'
    ) -> typing.List[dict]:

        view_of_person = self.has_a_view_on(other)
        view_of_person['value'] = get_random_positive_value()

        if view_of_person['random_value'] <= self.likelihood_of_being_wrong:
            view_of_person['attribute'] = random.choice(other.weaknesses)
        else:
            view_of_person['attribute'] = random.choice(other.strengths)

        return view_of_person

    def generate_negative_views(
        self, 
        other: 'Person',
        number_of_observations: int = 10
    ) -> typing.List[dict]:

        for _ in range(number_of_observations):
            yield self.has_a_negative_view_on(other)

    def generate_positive_views(
        self, 
        other: 'Person',
        number_of_observations: int = 10
    ) -> typing.List[dict]:

        for _ in range(number_of_observations):
            yield self.has_a_positive_view_on(other)


# #### Will Haffner
# 
#  - high threshold for conflict, low empathy, high standards. 
#  - Will gives the most dots. 
#  - Will’s weaknesses are Empathy, Assertive and Open-Minded, Listens Well. 
#  - Will’s strengths are Perceiving Problems, Analytical Thinking, Willing to Touch the Nerve, and Maintaining High Standards. 

# In[8]:


will_haffner = {
    'id': '1',
    'name': 'Will Haffner',
    'description': 'high threshold for conflict, low empathy, high standards.',
    'dot_factor': 1.0,
    'ranking_factor': 0.25,
    'weaknesses': [2, 6, 9],
    'strengths': [1, 10, 13, 20]
}


# #### Alex Chavez
# 
#  - highly principled, calls out badness. 
#  - Alex gives the most rankings. 
#  - Alex’s weaknesses are Maintaining High Standards, Empathy, Motivating Others. 
#  - His strengths are Perceiving Problems, Principled and Higher Level Thinking, Cuts Through it. 

# In[9]:


alex_chavez = {
    'id': '2',
    'name': 'Alex Chavez',
    'description': 'highly principled, calls out badness.',
    'dot_factor': 0.25,
    'ranking_factor': 1.0,
    'weaknesses': [6, 10, 12],
    'strengths': [3, 13, 15]
}


# #### Sophia Porrino
# 
#  - highly principled, calls out badness. 
#  - Sophia gives a mixed combination of Dots and Rankings. 
#  - Sophia’s weaknesses are Assertive and Open-Minded and Fighting to get in Synch. 
#  - Sophia’s strengths are Perceiving Problems and Principled and Higher Level Thinking. 

# In[10]:


sophia_porrino = {
    'id': '3',
    'name': 'Sophia Porrino',
    'description': 'highly principled, calls out badness.',
    'dot_factor': 0.5,
    'ranking_factor': 0.5,
    'weaknesses': [2, 7],
    'strengths': [13, 15]
}


# #### Chintan Mehta
# 
#  - less likely to give negative feedback. 
#  - Chintan only gives Dots. 
#  - Chintan’s weaknesses are Willing to Touch the Nerve, Synthesizing the Situation, Cuts through it. 
#  - Chintan’s strengths are Precise and Meticulous Problem Solving, Analytical Thinking, Linear Thinking, Pushing through to Results. 

# In[11]:


chintan_mehta = {
    'id': '4',
    'name': 'Chintan Mehta',
    'description': 'less likely to give negative feedback.',
    'dot_factor': 0.75,
    'ranking_factor': 0.0,
    'weaknesses': [3, 18, 20],
    'strengths': [1, 8, 14, 16]
}


# #### Vin Marshall
# 
#  - doesn’t really give Dots. Vin only gives Rankings. 
#  - Vin’s weaknesses are Willing to Touch the Nerve, Sizing People up, Manages Conflict to get at Truth. 
#  - Vin’s strengths are Thinking Strategically, Designing the Movie Script, and Determination. 

# In[12]:


vin_marshall = {
    'id': '5',
    'name': 'Vin Marshall',
    'description': 'less likely to give negative feedback.',
    'dot_factor': 0.25,
    'ranking_factor': 0.5,
    'weaknesses': [11, 17, 20],
    'strengths': [4, 5, 19]
}


# ### Start Generating Some Data

# In[13]:


will = Person(**will_haffner)
alex = Person(**alex_chavez)
sophia = Person(**sophia_porrino)
chintan = Person(**chintan_mehta)
vin = Person(**vin_marshall)


# ### Define a Scenario

# In[14]:


views_in_bulk = []


# In[15]:


views_in_bulk.extend([i for i in will.generate_negative_views(alex, number_of_observations=12)])
views_in_bulk.extend([i for i in will.generate_positive_views(alex, number_of_observations=3)])


# In[16]:


views_in_bulk.extend([i for i in alex.generate_negative_views(will, number_of_observations=6)])
views_in_bulk.extend([i for i in alex.generate_positive_views(will, number_of_observations=1)])


# In[17]:


scenario = pd.DataFrame(views_in_bulk)

attribute_lookup = {v: k for k, v in ATTRIBUTES.items()}
people_lookup = {v: k for k, v in PEOPLE_IDS.items()}

scenario['attribute_name'] = scenario['attribute'].apply(lambda x: attribute_lookup.get(x))
scenario['subject_name'] = scenario['subject'].apply(lambda x: people_lookup.get(x))
scenario['author_name'] = scenario['author'].apply(lambda x: people_lookup.get(x))


# In[18]:


scenario


# In[ ]:




