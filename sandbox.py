
class Test(object):
    ALGORITHM_STD_DEV_OF_BASELINE_VALS = lambda mean: mean + 1


a = [1,2,3]
b = map(Test.ALGORITHM_STD_DEV_OF_BASELINE_VALS, a)


print(list(b))

# db = Database_Handler(test_db=True)
# print(db.db.get('queen'))
