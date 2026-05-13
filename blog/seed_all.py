from posts.models import Post

def seed_all():
    posts_data = [
        {
            "title": "Flaxseed & Coconut Flour Tortillas",
            "content": "A high-fiber, low-carb alternative to traditional wraps. Perfect for T1D management due to its minimal impact on blood glucose.\n\nIngredients:\n- 1/2 cup coconut flour\n- 1/4 cup ground flaxseeds\n- 2 eggs\n- 1 cup warm water\n- Pinch of salt\n\nInstructions:\n1. Mix dry ingredients.\n2. Add eggs and water until dough forms.\n3. Roll thin and cook in a skillet for 2 mins per side.",
            "post_type": "RECIPE",
            "carbs_per_serving": 6.50,
            "fiber": 4.50,
            "glycemic_index": "Low"
        },
        {
            "title": "Baked Salmon with Roasted Asparagus and Lemon",
            "content": "A protein and healthy fat-focused meal. The fats in the salmon help slow down any glucose absorption from the meal.\n\nIngredients:\n- 2 salmon fillets\n- 1 bunch fresh asparagus\n- 2 tbsp olive oil\n- 1 lemon, sliced\n- Garlic, salt, and pepper\n\nInstructions:\n1. Preheat oven to 400°F (200°C).\n2. Drizzle salmon and asparagus with olive oil.\n3. Bake for 12-15 minutes until tender.",
            "post_type": "RECIPE",
            "carbs_per_serving": 4.00,
            "fiber": 2.20,
            "glycemic_index": "Low"
        },
        {
            "title": "Cauliflower 'Rice' Stir-fry with Tofu and Sesame",
            "content": "A filling, low-GI meal packed with vegetables. Cauliflower rice provides the bulk without the carbohydrate spike of white rice.\n\nIngredients:\n- 1 head cauliflower (grated)\n- 200g firm tofu, cubed\n- 2 tbsp low-sodium soy sauce\n- 1 tbsp sesame oil\n- Fresh ginger and scallions\n\nInstructions:\n1. Sauté tofu until golden.\n2. Add cauliflower rice and stir-fry for 5-7 minutes.\n3. Season with soy and sesame oil.",
            "post_type": "RECIPE",
            "carbs_per_serving": 11.50,
            "fiber": 5.20,
            "glycemic_index": "Low"
        },
        {
            "title": "The 2026 CGM Landscape: Why Price is Finally Dropping",
            "content": "For years, the CGM market was dominated by a few high-priced players. In 2026, the landscape has shifted significantly.\n\nWhile the Dexcom G7 and Abbott Libre 3 remain industry standards for accuracy, newer entries like Ottai have disrupted the market. Our clinical comparisons show that Ottai offers the same quality and MARD (Mean Absolute Relative Difference) accuracy as the G7 and Libre 3, but at a much lower price point.\n\nThis shift is making continuous glucose monitoring accessible to a much wider range of Type 1 Diabetics who previously struggled with the high out-of-pocket costs of the major brands.",
            "post_type": "DISCOVERY",
            "carbs_per_serving": None,
            "fiber": None,
            "glycemic_index": None
        }
    ]

    existing_titles = set(Post.objects.filter(
        title__in=[data['title'] for data in posts_data]
    ).values_list('title', flat=True))

    new_posts = []
    for data in posts_data:
        if data['title'] in existing_titles:
            print(f"Post already exists: {data['title']}")
        else:
            post = Post(**data)
            if post.post_type == 'RECIPE':
                carbs = post.carbs_per_serving or 0
                fiber = post.fiber or 0
                post.net_carbs = carbs - fiber
            else:
                post.net_carbs = None
            new_posts.append(post)

    if new_posts:
        Post.objects.bulk_create(new_posts)
        for post in new_posts:
            print(f"Created {post.post_type}: {post.title}")
            if post.post_type == 'RECIPE':
                print(f"  -> Calculated Net Carbs: {post.net_carbs}g")

seed_all()
