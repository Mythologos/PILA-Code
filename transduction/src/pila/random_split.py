import itertools

def randomly_split(data, proportions, generator):
    generator.shuffle(data)
    for data_slice in get_slices(len(data), proportions):
        yield data[data_slice]

def get_slices(length, proportions):
    cum_totals = list(itertools.accumulate(proportions))
    total = cum_totals[-1]
    prev_index = 0
    for cum_total in cum_totals:
        curr_index = round(cum_total * length / total)
        yield slice(prev_index, curr_index)
        prev_index = curr_index
