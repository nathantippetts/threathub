import flask
from virus_total import VirusTotal
from blogs import krebs, hackernews

app = flask.Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    posts = []
    posts.append(krebs())
    posts.append(hackernews())
    return flask.render_template("home.html", posts=posts, title="Home")


@app.route("/integrations")
def integrations():
    return flask.render_template("integrations.html", title="Integrations")


@app.route("/reputations")
def reputations():
    return flask.render_template("reputation.html", title="Reputation Lookup")


@app.route("/reputations/hash")
def hash_reputation():
    vt = VirusTotal()
    vt_hash_dict = vt.vt_hash_reputation()
    vt_results = vt.vt_parse_scan_results(vt_hash_dict)
    vt_totals = vt.vt_parse_scan_totals(vt_hash_dict)
    vt_query = vt.query
    return flask.render_template("reputation_results.html", title="Reputation Results", vt_totals=vt_totals, vt_hashes=vt_results, vt_query=vt_query)