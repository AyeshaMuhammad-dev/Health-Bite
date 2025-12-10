"""
OpenAI service for GPT-4.1 integration.
"""
import os
import json
from openai import AsyncOpenAI
from typing import Dict, Any, Optional

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class OpenAIService:
    """Service for OpenAI GPT-4.1 interactions."""
    
    async def chat_completion(
        self,
        query: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get chatbot response for nutrition/fitness queries.
        
        Args:
            query: User's question
            user_context: Optional user profile information
            
        Returns:
            AI-generated response
        """
        system_prompt = """You are a knowledgeable and friendly nutrition and fitness assistant for Health-Bite.
You provide accurate, helpful advice about:
- Healthy eating and meal planning
- Nutrition facts and calorie information
- Exercise and workout recommendations
- Weight management strategies
- Dietary restrictions and alternatives

Always provide practical, actionable advice. If asked about medical conditions, recommend consulting a healthcare professional."""

        user_prompt = query
        if user_context:
            context_str = f"\n\nUser Profile:\n- Age: {user_context.get('age', 'Not provided')}\n"
            if user_context.get('gender'):
                context_str += f"- Gender: {user_context['gender']}\n"
            if user_context.get('weight'):
                context_str += f"- Weight: {user_context['weight']} kg\n"
            if user_context.get('height'):
                context_str += f"- Height: {user_context['height']} cm\n"
            if user_context.get('goals'):
                context_str += f"- Goals: {user_context['goals']}\n"
            user_prompt = context_str + f"\nQuestion: {query}"

        try:
            response = await client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Using latest GPT-4 model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_diet_plan(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized diet plan based on user profile.
        
        Args:
            user_profile: User's age, gender, height, weight, goals
            
        Returns:
            Structured diet plan as JSON
        """
        system_prompt = """You are a professional nutritionist creating personalized diet plans.
Generate a comprehensive 7-day meal plan with:
- Breakfast, lunch, dinner, and 2 snacks per day
- Calorie counts for each meal
- Macronutrient breakdown (protein, carbs, fats)
- Simple, practical recipes

Return the response as valid JSON with this structure:
{
    "daily_calorie_target": number,
    "macros": {
        "protein_grams": number,
        "carbs_grams": number,
        "fats_grams": number
    },
    "weekly_plan": {
        "monday": [
            {"meal": "breakfast", "name": "...", "calories": number, "nutrients": {...}},
            ...
        ],
        ...
    }
}"""

        user_prompt = f"""Create a personalized diet plan for:
- Age: {user_profile.get('age', 'Not specified')}
- Gender: {user_profile.get('gender', 'Not specified')}
- Height: {user_profile.get('height', 'Not specified')} cm
- Weight: {user_profile.get('weight', 'Not specified')} kg
- Goals: {json.dumps(user_profile.get('goals', {}))}

Generate a healthy, balanced meal plan."""

        try:
            response = await client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=3000,
                response_format={"type": "json_object"},
            )
            
            content = response.choices[0].message.content.strip()
            plan = json.loads(content)
            
            # Also generate a workout plan
            workout_plan = await self._generate_workout_plan(user_profile)
            plan['workout_plan'] = workout_plan
            
            return plan
        except json.JSONDecodeError:
            raise Exception("Failed to parse AI-generated diet plan")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def _generate_workout_plan(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workout plan as part of diet plan generation."""
        system_prompt = """You are a fitness trainer creating personalized workout plans.
Generate a weekly workout plan with:
- Exercise name, sets, reps, duration
- Rest days
- Difficulty level

Return as JSON:
{
    "weekly_schedule": {
        "monday": [{"exercise": "...", "sets": number, "reps": "...", "duration": "..."}, ...],
        ...
    },
    "rest_days": ["sunday"],
    "difficulty": "beginner/intermediate/advanced"
}"""

        user_prompt = f"""Create a workout plan for:
- Age: {user_profile.get('age', 'Not specified')}
- Gender: {user_profile.get('gender', 'Not specified')}
- Weight: {user_profile.get('weight', 'Not specified')} kg
- Goals: {json.dumps(user_profile.get('goals', {}))}"""

        try:
            response = await client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"},
            )
            
            content = response.choices[0].message.content.strip()
            return json.loads(content)
        except Exception as e:
            # Return a basic workout plan if AI generation fails
            return {
                "weekly_schedule": {
                    "monday": [{"exercise": "Full body workout", "sets": 3, "reps": "10-12", "duration": "45 min"}],
                },
                "rest_days": ["sunday"],
                "difficulty": "intermediate"
            }
