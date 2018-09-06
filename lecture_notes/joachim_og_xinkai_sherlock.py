drugs = ["cocaine", 'morhphine', 'opium', 'heroin', 'alcohol', 'tobacco']
drugs += [el.title() for el in drugs]

with open("data/books/the_memoirs_of_sherlock_holmes.txt", encoding="utf8") as f:
    contents = f.read()

    for drug in drugs:

        count = contents.count(drug)
        print(f'{drug}: {count}')
