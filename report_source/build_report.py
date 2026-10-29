# Builds Project_Report.pdf. Re-run after replacing alu-logo.jpg:  python3 build_report.py
import hashlib, os, re, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
                                Preformatted, KeepTogether)
sys.path.insert(0, os.path.dirname(__file__))
from rep_text import Q1

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, ".."))
LOGO = os.path.join(PROJ, "alu-logo.jpg")
OUT = os.path.join(PROJ, "Project_Report.pdf")
STANDIN = "a6dce4c6366746b3bd84170898440af9514335fa53cfea100d6c53672cd6fc84"
HASH = hashlib.sha256(open(LOGO, "rb").read()).hexdigest()
def log(n): return open(os.path.join(HERE, n)).read().replace(STANDIN, HASH).replace("\u2714", "PASS")

NAME = "[Your Name]"; COURSE = "Cryptocurrency and Digital Assets - Assignment 1"
GITHUB = "https://github.com/[your-username]/alu-logo-registry"
VIDEO = "[paste your video link here]"

ss = getSampleStyleSheet()
B = ParagraphStyle("B", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=14.5, spaceAfter=7)
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=17, textColor=colors.HexColor("#8B0000"), spaceBefore=6, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12, textColor=colors.HexColor("#222222"), spaceBefore=8, spaceAfter=4)
H3 = ParagraphStyle("H3", parent=ss["Heading3"], fontSize=10.5, spaceBefore=6, spaceAfter=2)
BL = ParagraphStyle("BL", parent=B, leftIndent=14, bulletIndent=2, spaceAfter=3)
CAP = ParagraphStyle("CAP", parent=B, fontSize=8.5, textColor=colors.HexColor("#555555"), alignment=1)
TT = ParagraphStyle("TT", parent=ss["Title"], fontSize=24, textColor=colors.HexColor("#8B0000"))
def P(t, s=B): return Paragraph(t, s)
def bullets(items): return [Paragraph(i, BL, bulletText="\u2022") for i in items]

def term(text, size=7.3, caption=None):
    pre = Preformatted(text.strip("\n"), ParagraphStyle("T", fontName="Courier", fontSize=size, leading=size + 2.2, textColor=colors.HexColor("#E6E6E6")))
    t = Table([[pre]], colWidths=[16.6 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1E1E1E")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    out = [t]
    if caption: out.append(P(caption, CAP))
    return KeepTogether(out) if len(text.splitlines()) < 30 else out[0] if not caption else out

def shot_box(label):
    t = Table([[Paragraph("<b>[INSERT SCREENSHOT]</b><br/>" + label, ParagraphStyle("s", parent=B, fontSize=8, alignment=1))]], colWidths=[5.3 * cm], rowHeights=[3.2 * cm])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#8B0000")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF3F3")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return t

def table(rows, widths, head=True):
    cell = ParagraphStyle("c", parent=B, fontSize=8.8, leading=11.5, spaceAfter=0)
    data = [[Paragraph(str(c), cell) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if head: st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F0E0E0")))
    t.setStyle(TableStyle(st)); return t

def footer(c, d):
    c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
    c.drawString(2 * cm, 1.2 * cm, "ALU Logo Registry - " + COURSE); c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "Page %d" % d.page); c.restoreState()

s = []
# ---------------- Title ----------------
s += [Spacer(1, 3 * cm), P("Protecting the ALU Logo on the Ethereum Blockchain", TT),
      P("Cryptocurrency Exchange Exploration, ERC-721 Registration and ERC-20 Tokenisation", ParagraphStyle("st", parent=B, fontSize=13, alignment=1, leading=18)),
      Spacer(1, 1 * cm), P("<b>Course:</b> " + COURSE, ParagraphStyle("c", parent=B, alignment=1)),
      P("<b>Student:</b> " + NAME, ParagraphStyle("c", parent=B, alignment=1)),
      P("<b>Contracts:</b> ALUAssetRegistry.sol (ERC-721) and ALULogoToken.sol (ERC-20)", ParagraphStyle("c", parent=B, alignment=1)),
      P("<b>Tools:</b> Solidity 0.8.26, Hardhat 2.22.17, OpenZeppelin Contracts 5.0.2, Node.js", ParagraphStyle("c", parent=B, alignment=1)),
      Spacer(1, 1 * cm)]
toc = [["Part", "Contents"],
       ["Question 1", "Cryptocurrency exchange report (six steps)"],
       ["Question 2", "Abstract, Introduction, Blockchain Setup, Smart Contract Explanation, Tokenisation, Test Results, Conclusion, GitHub Link and Video"]]
s += [table(toc, [3 * cm, 13.6 * cm]), PageBreak()]

# ---------------- Question 1 ----------------
s += [P("Question 1: Cryptocurrency Exchange Report", H1),
      P("<i>This report is written for a classmate who has never used a cryptocurrency exchange. The platform I explored is Coinbase.</i>")]
for k, v in Q1.items():
    s += [P(k, H2), P(v)]
s += [Spacer(1, 4), table([["Screenshot 1", "Screenshot 2", "Screenshot 3"]], [5.5 * cm] * 3, head=False)]
s[-1] = Table([[shot_box("Identity verification page (Step 1)"), shot_box("Dashboard with BTC, ETH, USDC (Step 2)"), shot_box("Buy screen, history and security settings (Steps 4-6)")]], colWidths=[5.5 * cm] * 3)
s += [P("Replace each box with your own screenshot from the exchange.", CAP), PageBreak()]

# ---------------- Q2 ----------------
s += [P("Question 2: Protect the ALU Logo on the Ethereum Blockchain", H1), P("Abstract", H2),
      P("This project registers the official ALU logo on a local Ethereum blockchain so that its ownership and its exact file fingerprint (a SHA-256 hash) are recorded permanently and publicly. An ERC-721 smart contract (<b>ALUAssetRegistry</b>) stores the fingerprint so anyone can check whether a logo file is genuine, and an ERC-20 contract (<b>ALULogoToken</b>) splits ownership of the logo into 1,000,000 shares. Eight automated tests confirm that both contracts behave correctly. The system solves the problem of proving who owns a digital file and whether a copy has been changed.")]

s += [P("Introduction", H2),
      P("A university logo is valuable. If somebody edits it, uses it on a fake certificate or claims to own it, ALU's reputation can suffer. Today ALU would normally protect the logo with a copyright registration or by keeping a record in a database. Both have weaknesses:"),
      *bullets(["<b>A database</b> is controlled by one administrator. Records can be edited or deleted, by mistake, by a hacker or by someone with bad intentions, and nobody outside can prove that nothing was changed.",
                "<b>A copyright registration</b> is a paper or government process. It is slow, local to one country, and does not let an ordinary person quickly check if the PNG file on their computer is the real one.",
                "<b>A blockchain record</b> is public, timestamped and practically impossible to change. Anyone in the world can run a free check of a file against the stored fingerprint, without asking ALU and without trusting a single company."]),
      P("This does not replace copyright law; it adds a tamper-proof proof of existence and ownership date that is easy to verify. Tokenising the logo also lets ALU describe shared ownership clearly."),
      P("Blockchain Setup", H2),
      P("<b>Tools installed.</b> I installed <b>Node.js</b> (which runs JavaScript outside the browser and includes npm, the package manager), then created a project with <font face='Courier'>npm init</font>. I installed <b>Hardhat</b>, a development tool that compiles Solidity, runs tests and starts a local blockchain, together with <b>ethers.js</b> (a library to talk to the blockchain) and <b>OpenZeppelin Contracts</b> (audited, ready-made ERC-721 and ERC-20 code). The file <font face='Courier'>hardhat.config.js</font> tells Hardhat which Solidity version (0.8.26) to use. <font face='Courier'>npx hardhat compile</font> turns my <font face='Courier'>.sol</font> files into bytecode the blockchain understands, and <font face='Courier'>npx hardhat node</font> starts the local blockchain."),
      P("Running <font face='Courier'>npx hardhat node</font> printed 20 test wallets, each with 10,000 fake ETH. This is the screenshot that proves the node is running:"),
      term("\n".join(log("node.log").splitlines()[:19]), caption="Figure 1 - Local Hardhat node running and the test wallet addresses it generated"),
      P("<b>What is a local blockchain and why use one?</b> It is a private copy of an Ethereum-style network that runs only on my own computer. Developers use it because it is free (the ETH is fake), instant (blocks are created immediately instead of every 12 seconds), and safe: a bug in a contract cannot lose real money, and I can restart from scratch whenever I want. On the real Ethereum network every deployment costs real gas fees and mistakes cannot be undone, so it is used only after the code has been well tested."),
      P("<b>What is a wallet address?</b> A wallet address, such as <font face='Courier'>0xf39F...2266</font>, is a 42-character identifier derived from a public key. It is like an account number or email address on the blockchain: it identifies who owns ETH, NFTs and tokens, and who sent a transaction. Whoever holds the matching private key controls that address, so the private key must be kept secret. (Hardhat's test keys are public, so they must never be used on a real network.)")]

s += [PageBreak(), P("Smart Contract Explanation", H2),
      P("<b>What is a smart contract?</b> A smart contract is a program stored on the blockchain that runs exactly as written when someone sends it a transaction. A normal program runs on a server owned by a company; the owner can change the code, stop it, or alter its data. A smart contract runs on thousands of computers at once, nobody can secretly change it after deployment, its data is public, and it enforces its rules automatically (for example, it will always reject a duplicate hash). The cost is that every action costs gas and mistakes are permanent."),
      P("<b>What is an NFT and why ERC-721?</b> NFT stands for non-fungible token. \"Non-fungible\" means every token is unique and cannot be swapped one-for-one like a coin. ERC-721 is the Ethereum standard for such tokens: each token has its own ID and exactly one owner, and wallets and marketplaces already understand it. A logo is a single unique asset, so one NFT with ID 1 that stands for \"the official ALU logo\" is the right model. A fungible token like ERC-20 could not say \"this particular item\"."),
      P("<b>What is a SHA-256 hash?</b> SHA-256 is a mathematical function that reads any file and outputs a 256-bit fingerprint, written as 64 hexadecimal characters. The same file always gives the same hash, you cannot rebuild the file from the hash, and the function is designed so a tiny change in the input completely changes the output (the \"avalanche effect\"). To show this I changed <b>one pixel</b> of my logo file by one colour value. The hashes became completely different:", B)]
import subprocess
from PIL import Image
im = Image.open(LOGO).convert("RGB"); px = im.load(); r, g, b = px[5, 5]; px[5, 5] = (r, g, (b + 1) % 256)
tmp = "/tmp/_onepx.png"; im.save(tmp); H2h = hashlib.sha256(open(tmp, "rb").read()).hexdigest()
diff = sum(x != y for x, y in zip(HASH, H2h))
s += [term("Original logo : %s\nOne pixel off : %s\nHex characters that differ: %d of 64" % (HASH, H2h, diff), 7, "Figure 2 - Changing one pixel produces a totally different SHA-256 hash"),
      P("This is why <font face='Courier'>verifyLogoIntegrity</font> works: even a barely visible edit makes the hash different, so a fake logo is detected."),
      P("<b>Why can data on a blockchain not be changed?</b> Transactions are grouped into blocks, and each block contains the hash of the previous block, forming a chain. Changing old data would change that block's hash and break every block after it. Thousands of independent nodes keep copies and reject any chain that does not follow the rules, so an attacker would need to redo huge amounts of work or control most of the network. In my contract there is also no function that edits or deletes a stored record, so once registered, the data is permanent.")]

s += [P("How I generated the ALU logo hash", H3),
      P("I downloaded the official logo and saved it as <font face='Courier'>alu-logo.jpg</font>. I then generated its SHA-256 hash programmatically with Node.js' built-in <font face='Courier'>crypto</font> module (script <font face='Courier'>scripts/hash-logo.js</font>), which reads the raw bytes of the file and hashes them. The value is a real hash of the real file, not a placeholder. The same script is used by <font face='Courier'>deploy.js</font> and the tests, so the registered value always equals the file in the project."),
      term("$ npm run hash\nFile   : alu-logo.jpg\nSHA-256: 0x%s" % HASH, 7.3, "Figure 3 - SHA-256 hash of alu-logo.jpg (screenshot of the output)"),
      P("<b>Hash to verify independently:</b> <font face='Courier' size='7.5'>0x%s</font>" % HASH)]

s += [P("ALUAssetRegistry.sol - every part explained", H3),
      table([["Part", "What it does (plain English)"],
             ["struct AssetMetadata", "A record with five fields: the asset <b>name</b>, <b>file type</b>, <b>content hash</b> (bytes32), the <b>wallet that registered it</b> and the <b>Unix timestamp</b> of registration."],
             ["mapping tokenId => AssetMetadata", "Like a lookup table: give it a token ID and it returns the registration details, so anybody can look up an asset."],
             ["mapping bytes32 => bool (hashRegistered)", "Remembers which fingerprints are already used. This is how the contract knows a file was registered before."],
             ["registerAsset(name, fileType, hash)", "(1) Checks that inputs are not empty. (2) <b>Reverts</b> with the message \"Asset already registered: duplicate content hash\" if the hash exists. (3) Increments the counter to get a new token ID. (4) Saves the metadata and marks the hash as used. (5) Mints the NFT to the caller with <font face='Courier'>_safeMint()</font>. (6) Emits the <font face='Courier'>AssetRegistered</font> event. (7) Returns the new token ID. I save the data <i>before</i> minting because <font face='Courier'>_safeMint</font> may call another contract; this order (checks-effects-interactions) prevents re-entrancy attacks."],
             ["verifyLogoIntegrity(tokenId, hash)", "A <font face='Courier'>view</font> function. It compares the supplied hash with the stored one. Match: returns <b>true</b> and \"Logo is authentic.\" No match: returns <b>false</b> and \"Warning: logo does not match.\" It only reads data, so calling it costs no gas."],
             ["getAsset(tokenId)", "A <font face='Courier'>view</font> function that returns the complete AssetMetadata struct for a token."],
             ["totalRegistered()", "Small helper that returns how many assets have been registered."]],
            [5 * cm, 11.6 * cm]), Spacer(1, 6),
      P("<b>Deployment script (scripts/deploy.js).</b> It computes the logo hash from the real file, deploys <font face='Courier'>ALUAssetRegistry</font>, immediately calls <font face='Courier'>registerAsset(\"ALU Official Logo\", \"image/jpeg\", hash)</font>, and then deploys <font face='Courier'>ALULogoToken</font> using the deployer's address as the logo owner. Output of a run against the local node:"),
      term(log("deploy.log"), 7.3, "Figure 4 - Deployment: logo registered as token ID 1 and 1,000,000 ALUT minted")]

s += [PageBreak(), P("Tokenisation", H2),
      P("<b>What is tokenisation?</b> Tokenisation means representing the ownership of something, here the ALU logo, as digital tokens on a blockchain. Instead of one person owning 100%, ownership is cut into many equal pieces (shares) that can be held and transferred separately. The record of who owns how many is public and cannot be forged."),
      P("<b>ALULogoToken (ALUT).</b> The contract extends OpenZeppelin's ERC-20 and <font face='Courier'>Ownable</font>. The name is \"ALU Logo Token\", the symbol is ALUT, and the constructor mints the entire fixed supply of <b>1,000,000</b> tokens to the wallet given as <font face='Courier'>logoOwner</font>. There is no other mint function, so the supply can never increase. I set <font face='Courier'>decimals()</font> to 0 so one token is one whole share; this keeps the numbers simple (500,000 tokens = 50%)."),
      table([["Function", "Explanation"],
             ["distributeShares(recipient, amount)", "Only the owner can call it (<font face='Courier'>onlyOwner</font>). It requires amount &gt; 0, then moves that many ALUT from the owner's balance to the recipient and emits an event. This is how ALU hands out shares."],
             ["ownershipPercentage(account)", "A <font face='Courier'>view</font> function: <font face='Courier'>balance x 100 / totalSupply</font>. With 500,000 tokens it returns 50. Integer division rounds down, so holders of less than 1% see 0."]],
            [5 * cm, 11.6 * cm]), Spacer(1, 6),
      P("<b>Who at ALU might receive tokens, and why?</b>"),
      *bullets(["<b>The university administration / council</b> keeps the largest share, because ALU is the institutional owner of its brand.",
                "<b>Faculty members and department heads</b> could receive tokens as recognition of their work building the brand, for example in a design or marketing committee.",
                "<b>Student representatives or alumni association</b> could hold a small share, so the people who carry the logo also have a stake and a voice.",
                "<b>Founding partners or sponsors</b> could be issued tokens in return for supporting the university."]),
      P("<b>What does 100,000 ALUT out of 1,000,000 mean in practice?</b> The faculty member owns 10% of the logo's ownership shares. This is a verifiable record of a 10% stake: if ALU later decides that revenue from licensing the logo is shared by token holders, or that important decisions are voted on by token weight, that person would receive 10% of the revenue and have 10% of the voting power. The tokens can be shown, checked and transferred by wallet. Note that the legal meaning of the tokens must be agreed by ALU in a real agreement; the blockchain only records the numbers."),
      P("<b>ERC-721 versus ERC-20.</b>"),
      table([["", "ERC-721 (ALUAssetRegistry)", "ERC-20 (ALULogoToken)"],
             ["Type", "Non-fungible: every token is unique", "Fungible: every token is identical"],
             ["Tracks", "Which wallet owns token ID N", "How many tokens each wallet holds"],
             ["Divisible?", "No, one token = one whole item", "Yes, can be split into many holders"],
             ["Used here for", "Proving <b>what</b> the asset is (logo, hash, date)", "Describing <b>who owns how much</b> (shares)"]],
            [3 * cm, 6.8 * cm, 6.8 * cm]), Spacer(1, 6),
      P("I used ERC-721 for the registration because the logo is one unique item whose identity (its hash) must be fixed. I used ERC-20 for ownership because shares must be identical, countable and splittable, like shares of a company. The two together cover both \"what is it\" and \"who owns it\".")]

s += [P("Test Results", H2),
      P("I wrote eight automated tests in <font face='Courier'>test/ALUAssetRegistry.test.js</font> using Mocha and Chai: five for the registry (successful registration, duplicate rejection, true on correct hash, false on wrong hash, getAsset data) and three for the token (full supply minted, distributeShares, ownershipPercentage). All eight pass."),
      term(log("test.log"), 8, "Figure 5 - All eight tests passing (<font face='Courier'>npx hardhat test</font>)"),
      Spacer(1, 4), P("Security measures in the code: input validation, duplicate-hash protection, checks-effects-interactions ordering, <font face='Courier'>onlyOwner</font> access control on distributeShares, Solidity 0.8 built-in overflow checks, and use of audited OpenZeppelin base contracts instead of hand-written token logic.")]

s += [P("Conclusion", H2),
      P("<b>What I learned.</b> I learned how a cryptocurrency exchange verifies users and protects accounts, and how a smart contract differs from a normal program. Hashing taught me that a file can be proven authentic with just 64 characters, and writing tests showed me that blockchain code needs to be correct before deployment because it cannot be patched. I also learned the practical side of tooling: version conflicts between Hardhat plugins, OpenZeppelin v5 changes, and BigInt handling in ethers v6 all took time to solve (they are listed in the README)."),
      P("<b>What I would improve with more time.</b>"),
      *bullets(["Deploy to the Sepolia public testnet and verify the contracts on Etherscan.",
                "Link the two contracts so the token contract can check that the logo NFT exists, and store a metadata URI (for example on IPFS) with the NFT.",
                "Add a way to transfer or revoke the registry role for ALU's multi-signature wallet, so no single person controls the logo.",
                "Add more tests: non-existent token IDs, empty inputs, transfers between holders, and gas reports.",
                "Build the web interface (dApp) planned for the next assignment so non-technical users can drag in a file and verify it."]),
      P("GitHub Link", H2),
      P("Public repository with all code: <font color='#0033CC'><u>%s</u></font>" % GITHUB),
      P("Video", H2),
      P("Project video link: <font color='#0033CC'><u>%s</u></font>" % VIDEO)]

SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                  title="ALU Logo Registry - Project Report", author=NAME).build(s, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
