import requests_html as rh
import pypandoc

def generate_provider_pdf(url, filename, s=None):
    s = rh.HTMLSession() if not s else s
    r1 = s.get(url)

    html = ""
    anchors = r1.html.find('.nav-visible a')
    links = [a.absolute_links.pop() for a in anchors]
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

    print("generating pdf...")
    try:
        output = pypandoc.convert_text(html, "pdf", format="html", outputfile="./{}.pdf".format(filename), extra_args=['--pdf-engine=xelatex'])
    except Exception as e:
        print(e)

if __name__ == '__main__':
    s = rh.HTMLSession()
    r = s.get("https://www.terraform.io/docs/providers/index.html")
    providers = r.html.find('.table a')
    provider_pairs = [(p.absolute_links.pop(), p.text) for p in providers if p.absolute_links]
    for url, filename in provider_pairs:
        print(filename)
        generate_provider_pdf(url, filename, s=s)
