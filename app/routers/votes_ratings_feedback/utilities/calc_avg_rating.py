# This is for calculating the overall all categories average ratings
"""
formula:
average_rating_of_each_categories = sum of all the ratings of the one categories/total user did this.

and for overall average.
overall_average_rating = all categories overall rating/number of categories
"""
def calculate_average_rating_all_categories(rating):

    if rating:
        total_user_rating = len(rating)
        # making the empty list of all the categories so that I can store the number all ratings
        overall = []
        cleanliness = []
        safety = []
        crowd_behavior = []
        transport_access = []
        lightning = []
        facility_quality = []
        for all_categories in rating:
            overall.append(all_categories.overall)
            cleanliness.append(all_categories.cleanliness)
            safety.append(all_categories.safety)
            crowd_behavior.append(all_categories.crowd_behavior)
            transport_access.append(all_categories.transport_access)
            lightning.append(all_categories.lightning)
            facility_quality.append(all_categories.facility_quality)

        # creating each categories variable for storing the sum of all ratings.
        each_overall_sum = 0
        each_cleanliness_sum = 0
        each_safety_sum = 0
        each_crowd_behavior_sum = 0
        each_transport_access_sum = 0
        each_lightning_sum = 0
        each_facility_quality_sum = 0


        # now I am calculating the average rating of the categories

        # calculating average for overall ratings
        for each_rating in overall:
            each_overall_sum += each_rating

        # calculating the average of overall rating
        average_overall_rating = each_overall_sum/total_user_rating

        # calculating average for cleanliness
        for each_rating in cleanliness:
            each_cleanliness_sum += each_rating

        # calculating the average of cleanliness rating
        average_cleanliness_rating = each_cleanliness_sum/total_user_rating

        # calculating average for safety
        for each_rating in safety:
            each_safety_sum += each_rating

        # calculating the average of safety
        average_safety_rating = each_safety_sum/total_user_rating

        # calculating the average for crowd_behavior
        for each_rating in crowd_behavior:
            each_crowd_behavior_sum += each_rating

        average_crowd_behavior = each_crowd_behavior_sum/total_user_rating

        # calculating the average of transport rating
        for each_rating in transport_access:
            each_transport_access_sum += each_rating

        average_transport_access = each_transport_access_sum/total_user_rating

        # calculating the average of lightning rating
        for each_rating in lightning:
            each_lightning_sum += each_rating

        average_lightning = each_lightning_sum/total_user_rating

        for each_rating in facility_quality:
            each_facility_quality_sum += each_rating

        average_facility_quality = each_facility_quality_sum/total_user_rating

        # calculating the average of all categories


        # print(overall_average_rating)
        return total_user_rating, average_overall_rating, average_cleanliness_rating, average_safety_rating,average_crowd_behavior,average_transport_access, average_lightning, average_facility_quality

    else:
        return 0, 0, 0, 0, 0, 0, 0, 0
