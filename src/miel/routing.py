from re import match, sub, findall


def gen_re_pattern(url_pattern: str):
    fa = findall(r"\{(\w+)\}", url_pattern)
    print(tuple(fa))
    f = sub(r"\{\w+\}", r"([\\w\-]+)", url_pattern)
    f = f"^{f}$"
    print(f)

def test(pattern, path):
    m = match(r"^/abc/([\w\-]+)/def/([\w\-]+)$", path)
    print(m[1], m[2])


# s = "/hello/{my}"

# test("/abc/{id}/def/{di}", "/abc/15/def/hh")

gen_re_pattern("/abc/{id}/def/{di}")
