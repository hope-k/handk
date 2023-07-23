from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from inventory import models
from user_product_interaction.models import UserProductInteraction
from surprise import Reader, Dataset, KNNWithMeans
from surprise.model_selection import train_test_split
from pandas import DataFrame


def prepare_data():
    upi = UserProductInteraction.objects.all()
    upi_df = [(item.user, item.product, item.duration) for item in upi]
    upi_pd_df = DataFrame(upi_df, columns=['user', 'product', 'duration'])

    min_duration = upi_pd_df['duration'].min()
    max_duration = upi_pd_df['duration'].max()

    reader = Reader(rating_scale=(min_duration, max_duration))
    data = Dataset.load_from_df(DataFrame(upi_pd_df), reader=reader)
    trainset = data.build_full_trainset()
    _, testset = train_test_split(data, test_size=0.2)

    return trainset, testset


def similar_products(product_pk):
    products = models.Product.objects.exclude(pk=product_pk)
    product = models.Product.objects.get(pk=product_pk)

    # all features of products and features of product_pk
    features = [f"{prod.brand} {prod.category}" for prod in products]
    product_features = [f"{product.brand} {product.category}"]

    # use vectorizer to transform product_features
    vectorizer = TfidfVectorizer()
    features_vec = vectorizer.fit_transform(features)
    product_vec = vectorizer.fit(product_features)

    # get neighbors
    nbrs = NearestNeighbors(n_neighbors=5).fit(features_vec)
    distance, indices = nbrs.kneighbors(product_vec, n_neighbors=5)

    # similar products
    similar_prods = [products[idx] for idx in indices[0]]
    return similar_prods


def recommend_products(user_pk):
    trainset, testset = prepare_data()
    algo = KNNWithMeans(sim_options={
        'name': 'cosine',
        'user_based': True


    })
    algo.fit(trainset=trainset)
    # id surprise use
    user_inner_id = trainset.to_inner_uid(user_pk)
    neighbors = algo.get_neighbors(user_inner_id, k=5)

    recommendations = []
    for neighbor_id in neighbors:
        # Convert the Surprise inner user ID back to the original primary key
        neighbor_pk = trainset.to_raw_uid(neighbor_id)

        # Get the items that the neighbor has rated highly (you need to implement this)
        neighbor_top_items = models.Product.objects.filter(pk=neighbor_pk)

        # Add the neighbor's top items to the recommendation list
        recommendations.extend(neighbor_top_items)

    # It's also a good idea to filter out items that the current user has already rated to avoid redundant recommendations.
    # For example, you can get the items rated by the current user and remove them from the recommendations list.

    return recommendations
