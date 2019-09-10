import requests_html as rh
import pypandoc

def generate_provider_pdf(url, filename, s=None):
    s = rh.HTMLSession() if not s else s
    r1 = s.get(url)

    html = ""
    anchors = r1.html.find('.nav a')
    links = [a.absolute_links.pop() for a in anchors if a.absolute_links]
    links = filter(lambda href: href.find('/r/') != -1 or href.find('/d/') != -1, links) # filter out links not data or resource

    print("downloading...")
    for l1 in links:
        r2 = s.get(l1)
        # r2.html.render()
        div = r2.html.find('#inner', first=True)
        # with open("/tmp/b.html", "wt") as f:
        #     f.write(content.html)
        if div:
            html += div.html
    with open("/tmp/{}.html".format(filename), "wt") as f:
        f.write(html)

    print("generating pdf...")
    try:
        output = pypandoc.convert_text(html, "pdf", format="html", outputfile="./{}.pdf".format(filename), extra_args=['--pdf-engine=xelatex'])
    except Exception as e:
        print(e)

if __name__ == '__main__':
    s = rh.HTMLSession()
    r = s.get("https://www.terraform.io/docs/providers/index.html")
    providers = r.html.find('#inner a')
    provider_pairs = [(p.absolute_links.pop(), p.text) for p in providers if p.absolute_links]
    for url, filename in provider_pairs:
        if not url.startswith('https://www.terraform.io/docs/providers/'):
            continue
        print(filename, url)
        generate_provider_pdf(url, filename, s=s)
