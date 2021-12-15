import csv

def csv2html(query):
    results_html = ''
    count = 0
    with open("/home/tcy1999/mysite/out.csv", "r", encoding="UTF-8") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            if line[2]:
                count += 1
                tags = ''.join(['<li class="tag_item small">{}</li>'.format(x)
                    for x in line[2].split(',')[1:] if x])
                results_html += '<div class="card-deck my-3">\
                <div class="card mx-5" style="width: 18rem"><img src={} \
                class="card-img-top"><div class="card-body"><h3 class="card-title">\
                <a class="card-link" href={}>{}</a></h3><div class="bar"></div> \
                <p class="text-muted small">Category: {}</p>\
                <p class="card-text small">Author: {}</p><ul class="tagbox">{}</ul>\
                </div></div></div>'.format(line[6], line[3], line[1], line[4], 
                line[5].strip().rstrip(','), tags)

    if results_html:
        return results_html, count
    else:
        return '<p>No results found.</p>'
