from posts.models import Post

def seed_data():
    recipes = [
        {
            "title": "Flaxseed & Coconut Flour Tortillas",
            "content": "A high-fiber, low-carb alternative to traditional wraps.\n\nIngredients:\n- 1/2 cup coconut flour\n- 1/4 cup ground flaxseeds\n- 2 eggs\n- 1 cup warm water\n- Pinch of salt\n\nInstructions:\n1. Mix dry ingredients in a bowl.\n2. Add eggs and water, stirring until a dough forms.\n3. Let the dough rest for 5 minutes.\n4. Roll into small circles between parchment paper.\n5. Cook in a non-stick skillet over medium heat for 2 minutes per side.",
            "post_type": "RECIPE",
            "carbs_per_serving": 6.50,
            "fiber": 4.50,
            "glycemic_index": "Low"
        },
        {
            "title": "Baked Salmon with Roasted Asparagus and Lemon",
            "content": "A protein and healthy fat-focused meal with minimal impact on blood glucose.\n\nIngredients:\n- 2 salmon fillets\n- 1 bunch fresh asparagus\n- 2 tbsp olive oil\n- 1 lemon, sliced\n- Garlic, salt, and pepper\n\nInstructions:\n1. Preheat oven to 400°F (200°C).\n2. Place salmon and asparagus on a baking sheet.\n3. Drizzle with olive oil and top with lemon slices.\n4. Bake for 12-15 minutes until salmon flakes easily with a fork.",
            "post_type": "RECIPE",
            "carbs_per_serving": 4.00,
            "fiber": 2.20,
            "glycemic_index": "Low"
        },
        {
            "title": "Cauliflower 'Rice' Stir-fry with Tofu and Sesame",
            "content": "A filling, low-GI meal packed with vegetables and plant-based protein.\n\nIngredients:\n- 1 head cauliflower (grated into 'rice')\n- 200g firm tofu, cubed\n- 2 tbsp low-sodium soy sauce\n- 1 tbsp sesame oil\n- Fresh ginger and scallions\n\nInstructions:\n1. Press tofu to remove moisture, then sauté until golden.\n2. Add cauliflower rice and ginger to the pan.\n3. Stir-fry for 5-7 minutes until tender.\n4. Toss with soy sauce and sesame oil. Garnish with scallions.",
            "post_type": "RECIPE",
            "carbs_per_serving": 11.50,
            "fiber": 5.20,
            "glycemic_index": "Low"
        }
    ]

    existing_titles = set(Post.objects.filter(
        title__in=[r['title'] for r in recipes]
    ).values_list('title', flat=True))

    new_posts = []
    for data in recipes:
        if data['title'] not in existing_titles:
            # calculate net_carbs explicitly since bulk_create bypasses save()
            if data.get('post_type', 'DISCOVERY') == 'RECIPE':
                carbs = data.get('carbs_per_serving') or 0
                fiber = data.get('fiber') or 0
                data['net_carbs'] = carbs - fiber
            new_posts.append(Post(**data))
            print(f"Created recipe: {data['title']}")
        else:
            print(f"Recipe already exists: {data['title']}")

    if new_posts:
        Post.objects.bulk_create(new_posts)

if __name__ == "__main__":
    seed_data()
