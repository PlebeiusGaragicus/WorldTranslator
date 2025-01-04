import requests
# from lxml_html_clean import clean_html, Cleaner
from readability import Document

# https://github.com/buriy/python-readability

def scrape_url( url ):

    if not url.startswith("https://"):
        url = f"https://{url}"

    try:
        response = requests.get( url )

        # cleaner = Cleaner(style=False, links=True, add_nofollow=True, page_structure=False, safe_attrs_only=False)
        # page = cleaner.clean_html( response.content.decode('utf-8') )
        # doc = Document( page )

        doc = Document( response.content )
        article_markdown_contents = f""
        article_markdown_contents += doc.title()
        article_markdown_contents += doc.summary()

        return article_markdown_contents

    except Exception as e:
        print(e)
        return "Unable to scrape url"



GROUND_TRUTH = """

Insurance Crisis Looms as Prices Skyrocket and Providers Retreat
With major insurers like State Farm and Allstate withdrawing from the Californian market, an estimated 18 million Americans are currently without home insurance.

Staff
Insurance Crisis Looms as Prices Skyrocket and Providers Retreat
In a stark revelation recently reported in the Wall Street Journal, millions of American homeowners and drivers are confronting a looming insurance crisis. With insurance costs surging and leading companies withdrawing from high-risk areas to avoid financial ruin, the security of owning insurance is transforming into a precarious situation that many are struggling to navigate.

As the Wall Street Journal describes, securing car and home insurance has shifted from a habitual expense to a critical challenge. This precarious scenario is largely a byproduct of government policies that have inadvertently incentivized construction in hazard-prone regions while simultaneously increasing the risk in those very areas.

The insurance industry is grappling with a complex web of issues. On one hand, environmental policies have unintentionally led to the accumulation of dangerous underbrush, effectively setting the stage for potential mega fires across the United States. On the other hand, subsidized insurance for flood-prone areas has encouraged residential development in locations that should have been deemed unsuitable for such growth.

These factors have cornered insurance companies into making difficult decisions: either extend coverage to all and distribute the staggering costs of disaster claims across the board – which has led to premium hikes of up to 40% – or cut off coverage to the riskiest homes. The latter is becoming increasingly common, as evidenced by State Farm's $13 billion loss in underwriting last year, prompting them to retreat from markets like California.

The repercussions are dire. With major insurers like State Farm and Allstate withdrawing from the Californian market, an estimated 18 million Americans are currently without home insurance. This phenomenon, colloquially referred to as "going naked" within the industry, disproportionately affects low-income households for whom a loss could mean financial ruin.

The crisis isn't confined to home insurance. The car insurance sector is also struggling, with rates soaring by notable percentages across states like New York, New Jersey, and California. Nationally, car insurance costs have risen sixfold compared to inflation over the past year. This sharp increase is attributed to a combination of factors, including government emissions mandates and a spillover from the housing insurance debacle, as reinsurers – those insuring the insurance companies – pass on their losses.

The situation has reached a point where some consumers face exorbitant insurance costs, as highlighted by one woman's $18,000 yearly quote to insure her two homes and a 2011 minivan. The industry is witnessing the emergence of "insurance deserts," regions where providers are either pulling out or reducing their visibility and accessibility to avoid public relations fallout.

In states like Florida, the government-run insurer of last resort has become the top insurer, a testament to the severity of the crisis. Solutions to the issue would require sweeping reforms, but given the vested interests of lobbyists and activists, the likelihood of such change remains slim.

As the insurance landscape continues to deteriorate, consumers are left in a precarious position, with the situation predicted to worsen before any improvement is seen. The nation watches, waiting for a remedy to a crisis that underscores the interconnectedness of environmental policies, market economics, and the well-being of millions of Americans.

"""