"""Build the Puppy Panic lead-magnet ebook as HTML (and optionally PDF).

Usage:
    python build_ebook.py                 # writes output/Puppy_Panic_Survival_Guide.html
    python build_ebook.py --open          # ...and opens it in your browser
    python build_ebook.py --pdf           # ...and also writes a PDF (needs Playwright)

To change the ebook, edit the SETTINGS and PAGES sections below. You never
need to touch the HTML/CSS further down unless you want to restyle it.
"""

from __future__ import annotations

import argparse
import base64
import html
import mimetypes
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# SETTINGS - the things you will change most often
# ---------------------------------------------------------------------------

SETTINGS = {
    "brand": "PUPPY PANIC",
    "title": "The New Puppy Owner Survival Guide",
    "affiliate_url": "https://5065ekt-g52o1p0965oj1yv3wg.hop.clickbank.net/",
    "output_name": "Puppy_Panic_Survival_Guide",
    "images_dir": "images",  # drop cover.jpg, training.jpg etc. in here
    # Colours
    "accent": "#d97706",
    "accent_soft": "#fff7e6",
    "ink": "#1c2b39",
}

# ---------------------------------------------------------------------------
# PAGES - the ebook content, one dict per page, in order
#
# Block types you can use inside "blocks":
#   ("p", "text")                          paragraph
#   ("h3", "text")                         sub-heading
#   ("list", ["a", "b"])                   bullet list
#   ("checklist", ["a", "b"])              tick-box list (printable)
#   ("steps", ["first", "then"])           numbered how-to steps
#   ("grid", [("Title", "text"), ...])     small tip cards, two per row
#   ("dodont", ["do", ...], ["don't", ...])  Do / Avoid columns
#   ("card", "text")                       highlighted tip box
#   ("image", "file.jpg", "caption", "art")  photo from images/; until the
#                                          file exists a drawn illustration
#                                          ("art") is shown instead
#   ("table", ["head", ...], [[row], ...])    worksheet table
#   ("cta", "heading", "text", "button")   affiliate call-to-action box
#   ("note", "text")                       small print
#
# Illustrations ("art"): home, bone, ball, bulb, moon, heart
# ---------------------------------------------------------------------------

PAGES = [
    {
        "kind": "cover",
        "title": "The New Puppy Owner<br>Survival Guide",
        "subtitle": "A complete beginner handbook for raising a happier, "
                    "calmer and better-trained dog.",
        "image": ("cover.jpg", "", "heart"),
        "tagline": "16 chapters &middot; step-by-step training &middot; printable worksheets",
    },
    {"kind": "toc"},
    {
        "title": "Welcome To Puppy Parenthood",
        "blocks": [
            ("p", "Congratulations on welcoming a new puppy into your life. The first "
                  "weeks are important because your puppy is learning about your home, "
                  "your routine and your expectations. Everything they experience now "
                  "shapes the adult dog they will become."),
            ("p", "Many puppy behaviours that frustrate owners, like biting, crying at "
                  "night and chewing, are normal parts of development. They are not "
                  "signs that something is wrong with your puppy or with you. With "
                  "patience, consistency and the right guidance, you can turn each of "
                  "them into a learning moment."),
            ("h3", "The Three Golden Rules"),
            ("grid", [
                ("Reward what you like", "Behaviour that gets rewarded gets repeated. "
                 "Catch your puppy doing something right and pay them for it."),
                ("Manage what you don't", "Prevent mistakes before they happen with "
                 "gates, crates, lead and supervision."),
                ("Keep it short", "Three 5-minute sessions beat one 30-minute "
                 "session. End while your puppy still wants more."),
                ("Stay calm", "Puppies read your mood. A calm owner raises a calm "
                 "dog. Shouting only teaches them to fear you."),
            ]),
            ("h3", "How To Use This Guide"),
            ("p", "Read the chapters in order during your first week, then keep the "
                  "guide handy for the problem-solving pages. Print the worksheets at "
                  "the back and stick them on your fridge so the whole household "
                  "follows the same plan."),
            ("card", "<b>The Puppy Panic Promise:</b><br>Help owners understand their "
                     "dogs, create better habits and enjoy the journey."),
        ],
    },
    {
        "title": "Preparing Your Home",
        "blocks": [
            ("p", "Get everything ready before your puppy arrives so the first day is "
                  "about bonding, not shopping."),
            ("h3", "Shopping Checklist"),
            ("checklist", ["Crate or pen, big enough to stand up and turn around in",
                           "Soft bed and a blanket that smells of their litter (ask the breeder)",
                           "Food and water bowls",
                           "The same puppy food they are already eating",
                           "Small, soft training treats",
                           "3-4 chew toys of different textures",
                           "Collar with ID tag, plus a lightweight lead",
                           "Enzyme cleaner for accidents",
                           "Baby gates for rooms that are off-limits"]),
            ("h3", "Puppy-Proof Room By Room"),
            ("grid", [
                ("Living room", "Lift cables out of reach, move plants, and put "
                 "remote controls and shoes away."),
                ("Kitchen", "Lock bins and cleaning products away. Keep food off low "
                 "surfaces."),
                ("Bathroom", "Keep the toilet lid down and medicines stored high."),
                ("Garden", "Check fences for gaps and remove toxic plants and slug "
                 "pellets."),
            ]),
            ("card", "<b>Tip:</b> Get down on your hands and knees and look around. "
                     "Anything you can reach at puppy height, your puppy will find."),
        ],
    },
    {
        "title": "The First 48 Hours",
        "blocks": [
            ("image", "first-day.jpg", "A quiet, cosy base helps your puppy settle in.",
             "home"),
            ("h3", "Arrival Day"),
            ("steps", [
                "Take your puppy straight to their toilet spot outside and wait. "
                "Praise them quietly when they go.",
                "Let them explore one or two rooms at their own pace. Keep visitors "
                "away for the first few days.",
                "Show them their bed and water bowl, then let them nap as much as "
                "they want. Puppies sleep 18-20 hours a day.",
                "Start using their name in a happy voice whenever you feed, play or "
                "cuddle them.",
            ]),
            ("h3", "The First Night"),
            ("p", "Your puppy has just left their mother and littermates, so some "
                  "crying is normal. Place their crate or bed next to your bed for the "
                  "first nights so they can hear and smell you. A warm (not hot) water "
                  "bottle wrapped in a towel and a ticking clock can be comforting. "
                  "Expect one or two toilet trips during the night for the first weeks."),
        ],
    },
    {
        "title": "Understanding Puppy Behaviour",
        "blocks": [
            ("h3", "Why Puppies Bite"),
            ("p", "Puppies explore the world with their mouths, and they learned to "
                  "play by biting their littermates. Teething between about 3 and 6 "
                  "months makes it worse. The goal is not punishment. The goal is "
                  "teaching your puppy what they can bite instead."),
            ("h3", "Why Puppies Chew"),
            ("p", "Chewing relieves teething pain, burns energy and calms puppies down. "
                  "You cannot stop it, but you can direct it. Keep two or three chew "
                  "toys in every room and swap anything they should not have for "
                  "something they can have."),
            ("h3", "The Zoomies"),
            ("p", "Sudden bursts of wild running, usually in the evening, are a normal "
                  "way to release energy. Make sure the space is safe and let them run "
                  "it out. Frequent zoomies can mean your puppy is overtired and needs "
                  "a nap."),
            ("h3", "Reading Your Puppy's Body Language"),
            ("table", ["What you see", "What it usually means"], [
                ["Loose, wiggly body and soft eyes", "Relaxed and happy"],
                ["Play bow (front down, bottom up)", "Invitation to play"],
                ["Yawning, lip licking, looking away", "Unsure or stressed; give them space"],
                ["Tail tucked, ears flat, body low", "Frightened; remove them from the situation"],
                ["Stiff body, hard stare, freezing", "Uncomfortable; stop what is happening"],
            ]),
        ],
    },
    {
        "title": "Toilet Training Made Simple",
        "blocks": [
            ("p", "Toilet training is about timing. The more often your puppy goes in "
                  "the right place and gets rewarded, the faster they learn. Most "
                  "puppies are reliable by 4-6 months."),
            ("h3", "Take Your Puppy Out"),
            ("grid", [
                ("After waking", "From every nap as well as first thing in the morning."),
                ("After eating", "Usually within 15-30 minutes of a meal."),
                ("After play", "Excitement fills the bladder fast."),
                ("Every 1-2 hours", "A rough guide: puppies can hold on for about "
                 "their age in months plus one, in hours."),
            ]),
            ("h3", "The Routine"),
            ("steps", [
                "Go to the same spot every time, on lead, and stand still.",
                "Say a cue word such as \"be quick\" while they sniff.",
                "The moment they finish, praise and give a treat right there.",
                "If nothing happens within 5 minutes, go back in, watch them closely "
                "and try again in 10 minutes.",
            ]),
            ("h3", "When Accidents Happen"),
            ("dodont",
             ["Calmly pick them up and take them outside",
              "Clean with an enzyme cleaner to remove the smell",
              "Go out more often for a few days"],
             ["Shouting or rubbing their nose in it",
              "Using ammonia-based cleaners, which smell like urine",
              "Punishing an accident you did not see happen"]),
        ],
    },
    {
        "title": "Puppy Training Foundations",
        "blocks": [
            ("p", "Puppies can start learning the day they come home. Use food, toys "
                  "and praise to show them what you want, and keep every session short "
                  "and fun."),
            ("h3", "Name Recognition"),
            ("steps", [
                "Say your puppy's name once in a happy voice.",
                "The moment they look at you, say \"yes!\" and give a treat.",
                "Repeat 10 times, a few times a day, in different rooms.",
            ]),
            ("h3", "Sit"),
            ("steps", [
                "Hold a treat at your puppy's nose.",
                "Slowly move it up and back over their head. As their head goes up, "
                "their bottom goes down.",
                "The moment they sit, say \"yes!\" and give the treat.",
                "Once they follow the treat every time, say \"sit\" just before you move "
                "your hand.",
            ]),
            ("h3", "Come"),
            ("steps", [
                "Start indoors, a few steps away. Crouch down and call their name "
                "followed by \"come!\" in an exciting voice.",
                "Reward with something extra special every time they reach you.",
                "Slowly increase the distance, then practise in the garden.",
            ]),
            ("card", "<b>Never</b> call your puppy to you for something they dislike, "
                     "like a bath or the end of play. Coming to you should always be "
                     "the best decision they make."),
        ],
    },
    {
        "title": "Stay, Leave It And Settle",
        "blocks": [
            ("h3", "Stay"),
            ("steps", [
                "Ask for a sit. Show a flat palm and say \"stay\".",
                "Wait one second, then say \"yes!\" and reward while they are still sitting.",
                "Build up slowly: 2 seconds, 5 seconds, 10 seconds.",
                "Only then add distance: one step back, return, reward.",
            ]),
            ("h3", "Leave It"),
            ("steps", [
                "Hold a treat in a closed fist. Let your puppy sniff and lick.",
                "Wait. The moment they back off or look away, say \"yes!\" and reward "
                "from your other hand.",
                "When they back off straight away, add the words \"leave it\".",
                "Progress to a treat on the floor, covered by your hand if needed.",
            ]),
            ("h3", "Settle On A Mat"),
            ("steps", [
                "Sit on a chair with your puppy on lead and a mat or blanket on the floor.",
                "Ignore them and reward calmly whenever they lie down on the mat.",
                "Over a few days, reward longer and more relaxed settles.",
            ]),
            ("card", "Short daily training sessions are more effective than long "
                     "frustrating sessions. Aim for 3-5 minutes, 3 times a day."),
        ],
    },
    {
        "title": "Socialisation: The Window That Matters",
        "blocks": [
            ("p", "Between about 3 and 14 weeks old, puppies accept new experiences "
                  "easily. What they meet calmly now, they are less likely to fear "
                  "later. Aim for lots of short, positive introductions. Ask your vet "
                  "when it is safe for your puppy to walk in public places and meet "
                  "other dogs; until then, carry them and invite people over."),
            ("h3", "Socialisation Checklist"),
            ("checklist", [
                "People: men, women, children, people in hats, beards, uniforms",
                "Sounds: vacuum, doorbell, washing machine, traffic, fireworks recordings",
                "Surfaces: grass, gravel, tiles, wet ground, metal grates",
                "Handling: paws, ears, mouth, brushing, nail trims",
                "Places: car rides, a café, the vet's waiting room (just for treats)",
                "Animals: a calm, vaccinated adult dog, cats if you have them",
                "Things: umbrellas, bikes, pushchairs, wheelie bins",
            ]),
            ("dodont",
             ["Let your puppy approach in their own time",
              "Pair every new thing with treats",
              "Keep introductions short and end on a good note"],
             ["Forcing them towards something scary",
              "Crowds of strangers all at once",
              "Rough play with unknown dogs"]),
        ],
    },
    {
        "title": "Your Puppy's First 30 Days",
        "blocks": [
            ("h3", "Week 1: Settle In"),
            ("list", ["Build trust with calm handling and lots of sleep",
                      "Set a toilet routine and mealtimes",
                      "Teach name recognition",
                      "Introduce the crate or pen with meals and treats"]),
            ("h3", "Week 2: Build Habits"),
            ("list", ["Start sit and the first steps of come",
                      "Practise short periods alone (a few minutes in another room)",
                      "Begin handling practice: paws, ears, collar"]),
            ("h3", "Week 3: Grow Confidence"),
            ("list", ["Add stay and leave it",
                      "Introduce new sounds, surfaces and visitors",
                      "Try the first brain games from this guide"]),
            ("h3", "Week 4: Practise Everywhere"),
            ("list", ["Repeat every command in new rooms and the garden",
                      "Work on settle while you eat or watch TV",
                      "Review your progress tracker and pick your next goal"]),
            ("card", "Every puppy learns at their own speed. If you fall behind, "
                     "simply repeat the week. Consistency matters more than speed."),
        ],
    },
    {
        "title": "Solving Common Problems",
        "blocks": [
            ("h3", "Crying At Night"),
            ("list", ["Keep your puppy close to you for the first nights",
                      "Tire them out with play and a toilet trip before bed",
                      "Give a quiet toilet break if they wake, then straight back to bed",
                      "Move the crate further away gradually over a few weeks"]),
            ("h3", "Biting Hands"),
            ("list", ["When teeth touch skin, say \"oops\", stop play for a few seconds",
                      "Offer a tug toy or chew instead",
                      "If they are overexcited, it is usually nap time"]),
            ("h3", "Jumping Up"),
            ("list", ["Turn away and ignore jumping",
                      "Reward the moment all four paws are on the floor",
                      "Ask visitors to do the same so the rule is consistent"]),
            ("h3", "Chewing Furniture"),
            ("list", ["Supervise, or use a pen when you cannot watch",
                      "Swap the item for a chew toy and praise",
                      "Offer frozen chews during teething"]),
            ("h3", "Pulling On The Lead"),
            ("list", ["Stop walking whenever the lead goes tight",
                      "Move forward again when it goes slack",
                      "Reward them for walking by your side"]),
        ],
    },
    {
        "title": "Brain Training For Dogs",
        "blocks": [
            ("p", "Dogs need mental exercise as well as physical exercise. Ten minutes "
                  "of brain work can tire a puppy as much as a walk, and it builds "
                  "focus, confidence and problem-solving."),
            ("image", "brain-games.jpg", "A tired brain is a calm puppy.", "bulb"),
            ("h3", "Five Games To Try This Week"),
            ("grid", [
                ("Find it", "Toss a treat a short way and say \"find it\". Then hide "
                 "treats around the room for them to sniff out."),
                ("Cup game", "Hide a treat under one of three cups and let your "
                 "puppy choose. Reward correct guesses."),
                ("Muffin tin puzzle", "Put treats in a muffin tin and cover each "
                 "one with a tennis ball."),
                ("Snuffle towel", "Roll treats inside an old towel and let them "
                 "unroll it."),
                ("Touch", "Teach them to nose-touch your palm. It becomes a handy "
                 "way to move your puppy anywhere."),
                ("Name the toy", "Say a toy's name each time you play with it. "
                 "Soon they can fetch it by name."),
            ]),
        ],
    },
    {
        "title": "Bonus: 7-Day Puppy Training Challenge",
        "blocks": [
            ("p", "Five to ten minutes a day. Tick each day off as you go."),
            ("table", ["Day", "Focus", "Done"], [
                ["1", "Name game: say their name, reward eye contact", ""],
                ["2", "Sit: lure with a treat, reward the moment they sit", ""],
                ["3", "Handling: gently touch paws and ears, reward calm", ""],
                ["4", "Come: short recalls indoors, big rewards", ""],
                ["5", "Leave it: reward looking away from a treat in your hand", ""],
                ["6", "Settle: reward lying calmly on their bed", ""],
                ["7", "Review: practise every skill in a new room", ""],
            ]),
            ("image", "challenge.jpg", "Small wins every day add up fast.", "ball"),
            ("card", "<b>Finished the week?</b> Start again, this time practising in "
                     "the garden or with a friend watching."),
        ],
    },
    {
        "title": "Bonus: Daily Puppy Schedule",
        "blocks": [
            ("p", "Here is a sample day for a puppy of 8-12 weeks. Adjust the times to "
                  "fit your home. Consistency is what matters most."),
            ("table", ["Time", "Activity", "Your time"], [
                ["7:00", "Wake up + toilet break", ""],
                ["7:15", "Breakfast, then toilet break", ""],
                ["7:45", "Play and a 5-minute training session", ""],
                ["8:30", "Nap in crate or pen", ""],
                ["10:30", "Toilet break + explore the garden", ""],
                ["12:00", "Lunch, toilet break, then nap", ""],
                ["15:00", "Brain game + toilet break", ""],
                ["17:00", "Dinner, then toilet break", ""],
                ["18:00", "Family time and handling practice", ""],
                ["20:00", "Calm wind-down with a chew", ""],
                ["22:00", "Last toilet break + bed", ""],
            ]),
            ("note", "Add a toilet break after every nap, meal and play session, "
                     "plus once or twice at night for the first few weeks."),
        ],
    },
    {
        "title": "My Puppy Profile",
        "blocks": [
            ("p", "Fill this in and keep it somewhere handy, such as on the fridge."),
            ("table", [], [["Name", ""], ["Breed", ""], ["Date of birth", ""],
                           ["Date they came home", ""], ["Favourite treat", ""],
                           ["Favourite toy", ""], ["Vet name + phone", ""],
                           ["Next vaccination", ""], ["Microchip number", ""],
                           ["My #1 training goal", ""]]),
            ("image", "profile.jpg", "Stick your favourite photo of your puppy here.",
             "heart"),
        ],
    },
    {
        "title": "My Puppy Progress Tracker",
        "blocks": [
            ("p", "Score each skill every week: 1 = just started, 2 = getting there, "
                  "3 = does it every time."),
            ("table", ["Skill", "Week 1", "Week 2", "Week 3", "Week 4"], [
                [skill, "", "", "", ""]
                for skill in ["Name", "Sit", "Come", "Stay", "Leave It", "Settle",
                              "Toilet outside", "Loose lead", "Calm greetings",
                              "Alone time"]
            ]),
            ("h3", "Notes"),
            ("table", [], [[""], [""], [""]]),
        ],
    },
    {
        "title": "Continue Your Training Journey",
        "blocks": [
            ("p", "You now have the foundations: a routine, first commands and a plan "
                  "for the most common problems. The next step is to keep your puppy's "
                  "brain busy as they grow."),
            ("p", "For owners who want a structured approach with progressive "
                  "exercises, explore Brain Training For Dogs. It builds on the games "
                  "in this guide with step-by-step lessons for focus, impulse control "
                  "and obedience."),
            ("cta", "Explore Brain Training For Dogs",
                    "A guided training system for developing focus, engagement and "
                    "learning.",
                    "Start Training Your Dog"),
            ("image", "next-steps.jpg", "Keep learning together.", "bone"),
            ("note", "Disclosure: Puppy Panic may earn a commission if you purchase "
                     "through this link at no extra cost to you. This guide is general "
                     "information and not a substitute for advice from your vet."),
        ],
    },
    {
        "kind": "cover",
        "title": "Your Puppy Journey<br>Starts Today",
        "subtitle": "Every great dog begins with patience, consistency and love.",
        "image": ("back-cover.jpg", "", "moon"),
    },
]

# ---------------------------------------------------------------------------
# Illustrations - shown wherever a photo has not been added yet
# ---------------------------------------------------------------------------

PUPPY = """
<g transform="translate(%(x)s,%(y)s)">
  <ellipse cx="-44" cy="-6" rx="20" ry="40" fill="#8b5a2b" transform="rotate(20 -44 -6)"/>
  <ellipse cx="44" cy="-6" rx="20" ry="40" fill="#8b5a2b" transform="rotate(-20 44 -6)"/>
  <circle r="50" fill="#e8b77a"/>
  <ellipse cx="-20" cy="-10" rx="17" ry="15" fill="#c98f4f"/>
  <ellipse cy="22" rx="28" ry="20" fill="#f7e2c2"/>
  <circle cx="-19" cy="-9" r="7" fill="#1c2b39"/><circle cx="-17" cy="-11" r="2.2" fill="#fff"/>
  <circle cx="19" cy="-9" r="7" fill="#1c2b39"/><circle cx="21" cy="-11" r="2.2" fill="#fff"/>
  <ellipse cy="12" rx="9" ry="6.5" fill="#1c2b39"/>
  <path d="M0 18 v8 M-11 27 q11 9 22 0" stroke="#1c2b39" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M-5 30 q5 12 10 0 z" fill="#f28b82"/>
</g>"""

PROPS = {
    "bone": '<g transform="translate(330,150) rotate(-20)" fill="#fff" stroke="#e2c9a0" stroke-width="3">'
            '<rect x="-38" y="-9" width="76" height="18" rx="9"/><circle cx="-38" cy="-10" r="12"/>'
            '<circle cx="-38" cy="10" r="12"/><circle cx="38" cy="-10" r="12"/><circle cx="38" cy="10" r="12"/></g>',
    "ball": '<g transform="translate(335,145)"><circle r="30" fill="%(accent)s"/>'
            '<path d="M-28 -10 q28 22 56 0 M-28 10 q28 -22 56 0" stroke="#fff" stroke-width="4" fill="none"/></g>',
    "bulb": '<g transform="translate(335,95)"><circle r="30" fill="#fde68a"/><rect x="-12" y="26" width="24" height="16" rx="4" fill="#94a3b8"/>'
            '<path d="M0 -48 v-10 M40 -30 l8 -8 M-40 -30 l-8 -8 M48 0 h10 M-48 0 h-10" stroke="%(accent)s" stroke-width="4" stroke-linecap="round"/></g>',
    "moon": '<g transform="translate(330,70)"><circle r="28" fill="#fde68a"/><circle cx="12" cy="-8" r="24" fill="%(accent_soft)s"/></g>'
            '<g fill="%(accent)s"><circle cx="270" cy="45" r="4"/><circle cx="380" cy="120" r="3"/><circle cx="60" cy="60" r="4"/></g>',
    "home": '<g transform="translate(335,150)"><path d="M-40 0 L0 -36 L40 0 Z" fill="%(accent)s"/>'
            '<rect x="-30" y="0" width="60" height="42" fill="#fff" stroke="#e2c9a0" stroke-width="3"/>'
            '<rect x="-9" y="16" width="18" height="26" fill="#8b5a2b"/></g>',
    "heart": '<path transform="translate(330,70) scale(1.4)" d="M0 10 C-20 -6 -12 -22 0 -12 C12 -22 20 -6 0 10 Z" fill="#f28b82"/>'
             '<path transform="translate(80,160) scale(0.9)" d="M0 10 C-20 -6 -12 -22 0 -12 C12 -22 20 -6 0 10 Z" fill="%(accent)s"/>',
}

PAW = ('<g fill="%(accent)s" opacity=".12" transform="translate(%(x)s,%(y)s) rotate(%(r)s)">'
       '<ellipse rx="11" ry="9" cy="8"/><circle cx="-11" cy="-6" r="5"/><circle cx="-4" cy="-13" r="5"/>'
       '<circle cx="4" cy="-13" r="5"/><circle cx="11" cy="-6" r="5"/></g>')


def illustration(art: str, cfg: dict) -> str:
    paws = "".join(PAW % {**cfg, "x": x, "y": y, "r": r} for x, y, r in
                   [(40, 190, -20), (90, 40, 15), (300, 30, 30), (375, 200, -10), (250, 205, 20)])
    return (f'<svg viewBox="0 0 420 230" role="img" aria-label="Puppy illustration">'
            f'<rect width="420" height="230" fill="{cfg["accent_soft"]}"/>{paws}'
            f'<ellipse cx="200" cy="205" rx="90" ry="10" fill="#000" opacity=".06"/>'
            f'{PUPPY % {"x": 200, "y": 125}}{PROPS.get(art, "") % cfg}</svg>')


# ---------------------------------------------------------------------------
# Rendering - no need to edit below here for content changes
# ---------------------------------------------------------------------------

CSS = """
@page { size: A4; margin: 0; }
:root { --accent: %(accent)s; --accent-soft: %(accent_soft)s; --ink: %(ink)s; }
* { box-sizing: border-box; }
body {
  margin: 0; background: #e9ecef; color: #333;
  font-family: "Segoe UI", Arial, Helvetica, sans-serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.book { max-width: 210mm; margin: auto; }
.page {
  background: #fff; width: 100%%; min-height: 297mm; margin: 25px auto;
  padding: 18mm 18mm 22mm; position: relative; overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,.08);
}
.page::before {  /* gold accent bar */
  content: ""; position: absolute; top: 0; left: 0; right: 0; height: 8px;
  background: var(--accent);
}
.cover {
  background: linear-gradient(135deg, var(--accent-soft), #fff);
  text-align: center; display: flex; flex-direction: column; justify-content: center;
}
.brand { color: var(--accent); font-size: 20px; letter-spacing: 3px; font-weight: bold; }
h1 { font-size: 46px; line-height: 1.15; color: var(--ink); margin: 20px 0; }
h2 {
  color: var(--ink); font-size: 28px; margin: 0 0 14px;
  border-bottom: 3px solid var(--accent); padding-bottom: 10px;
}
h3 { color: var(--accent); margin: 18px 0 4px; font-size: 18px; }
p, li { font-size: 16px; line-height: 1.65; margin: 7px 0; }
ul { margin: 6px 0; padding-left: 22px; }
.subtitle { font-size: 22px; }
.figure {
  margin: 16px 0; border-radius: 18px; overflow: hidden; background: var(--accent-soft);
}
.figure img, .figure svg { display: block; width: 100%%; height: 200px; object-fit: cover; }
.cover .figure svg, .cover .figure img { height: 320px; }
.figure figcaption { padding: 8px 16px; font-size: 13px; color: #8a6a3b; font-style: italic; }
.card {
  background: var(--accent-soft); border-left: 6px solid var(--accent);
  padding: 14px 18px; margin: 16px 0; border-radius: 12px; font-size: 15px; line-height: 1.6;
}
.checklist { list-style: none; padding: 14px 18px; background: #f8fafc; border-radius: 15px; }
.checklist li::before {
  content: ""; display: inline-block; width: 14px; height: 14px; margin-right: 12px;
  border: 2px solid var(--accent); border-radius: 4px; vertical-align: -2px;
}
.steps { list-style: none; counter-reset: step; padding: 0; margin: 8px 0; }
.steps li { counter-increment: step; position: relative; padding-left: 38px; margin: 8px 0; }
.steps li::before {
  content: counter(step); position: absolute; left: 0; top: 1px; width: 26px; height: 26px;
  border-radius: 50%%; background: var(--ink); color: #fff; font-size: 13px;
  font-weight: bold; display: flex; align-items: center; justify-content: center;
}
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 10px 0; }
.grid div { background: #f8fafc; border-radius: 12px; padding: 12px 14px; font-size: 14px; line-height: 1.5; }
.grid b { display: block; color: var(--ink); margin-bottom: 3px; font-size: 15px; }
.dodont { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 12px 0; }
.dodont div { border-radius: 12px; padding: 12px 14px; }
.dodont .do { background: #ecfdf5; } .dodont .dont { background: #fef2f2; }
.dodont b { display: block; margin-bottom: 4px; }
.dodont .do b { color: #047857; } .dodont .dont b { color: #b91c1c; }
.dodont ul { padding-left: 18px; }
.dodont li { font-size: 14px; }
.toc ol { padding-left: 0; list-style: none; counter-reset: toc; }
.toc li {
  counter-increment: toc; display: flex; gap: 12px; padding: 9px 0; font-size: 16px;
  border-bottom: 1px dotted #cbd5e1;
}
.toc li::before { content: counter(toc, decimal-leading-zero); color: var(--accent); font-weight: bold; }
.toc a { color: inherit; text-decoration: none; }
.cta {
  background: var(--ink); color: #fff; padding: 28px; border-radius: 20px;
  text-align: center; margin: 20px 0;
}
.cta h3 { color: #fff; font-size: 22px; margin-top: 0; }
.cta a {
  display: inline-block; background: var(--accent); color: #fff; padding: 14px 30px;
  border-radius: 30px; text-decoration: none; margin-top: 10px; font-weight: bold;
}
.note { font-size: 12px; color: #666; }
table { width: 100%%; border-collapse: collapse; margin: 10px 0; }
td, th { border: 1px solid #ddd; padding: 9px 10px; font-size: 14px; text-align: left; }
th { background: var(--accent-soft); color: var(--ink); }
.form td:first-child { width: 35%%; font-weight: bold; background: #f8fafc; }
td:empty::after { content: "\\00a0"; }
.footer {
  position: absolute; bottom: 10mm; left: 18mm; right: 18mm;
  display: flex; justify-content: space-between; color: #999; font-size: 12px;
}
@media print {
  body { background: #fff; }
  .page { margin: 0; box-shadow: none; height: 297mm; page-break-after: always; break-after: page; }
}
@media (max-width: 600px) {
  .page { padding: 30px 18px 60px; min-height: auto; margin: 10px auto; }
  .footer { left: 18px; right: 18px; bottom: 15px; }
  .grid, .dodont { grid-template-columns: 1fr; }
  h1 { font-size: 34px; } h2 { font-size: 23px; }
  td, th { padding: 7px 6px; font-size: 13px; }
}
"""

esc = html.escape  # used for text that should never contain HTML


def slug(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")


def image_html(filename: str, caption: str, art: str, cfg: dict, images_dir: Path) -> str:
    """Embed the photo if it exists, otherwise draw an illustration."""
    path = images_dir / filename
    if path.is_file():
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        data = base64.b64encode(path.read_bytes()).decode()
        visual = f'<img src="data:{mime};base64,{data}" alt="{esc(caption)}">'
    else:
        visual = illustration(art, cfg)
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="figure">{visual}{cap}</figure>'


def block_html(block: tuple, cfg: dict, images_dir: Path) -> str:
    kind, *args = block
    if kind == "p":
        return f"<p>{args[0]}</p>"
    if kind == "h3":
        return f"<h3>{args[0]}</h3>"
    if kind in ("list", "checklist", "steps"):
        tag, cls = ("ol", ' class="steps"') if kind == "steps" else ("ul", "")
        if kind == "checklist":
            cls = ' class="checklist"'
        items = "".join(f"<li>{item}</li>" for item in args[0])
        return f"<{tag}{cls}>{items}</{tag}>"
    if kind == "grid":
        cells = "".join(f"<div><b>{t}</b>{text}</div>" for t, text in args[0])
        return f'<div class="grid">{cells}</div>'
    if kind == "dodont":
        do = "".join(f"<li>{i}</li>" for i in args[0])
        dont = "".join(f"<li>{i}</li>" for i in args[1])
        return (f'<div class="dodont"><div class="do"><b>&#10003; Do</b><ul>{do}</ul></div>'
                f'<div class="dont"><b>&#10007; Avoid</b><ul>{dont}</ul></div></div>')
    if kind == "card":
        return f'<div class="card">{args[0]}</div>'
    if kind == "note":
        return f'<p class="note">{args[0]}</p>'
    if kind == "image":
        return image_html(*args, cfg, images_dir)
    if kind == "table":
        head, rows = args
        thead = "<tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>" if head else ""
        body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
        cls = "" if head else ' class="form"'  # no header = label/answer form
        return f"<table{cls}>{thead}{body}</table>"
    if kind == "cta":
        heading, text, button = args
        return (f'<div class="cta"><h3>{heading}</h3><p>{text}</p>'
                f'<a href="{esc(cfg["affiliate_url"])}" target="_blank" '
                f'rel="sponsored noopener">{button}</a></div>')
    raise ValueError(f"Unknown block type: {kind!r}")


def build_html(cfg: dict, pages: list[dict], images_dir: Path) -> str:
    chapters = [p for p in pages if p.get("kind", "chapter") == "chapter"]
    sections = []
    for number, page in enumerate(pages, start=1):
        kind = page.get("kind", "chapter")
        footer = (f'<div class="footer"><span>{esc(cfg["brand"])}</span>'
                  f"<span>{number}</span></div>")
        if kind == "cover":
            image = image_html(*page["image"], cfg, images_dir) if page.get("image") else ""
            tagline = f'<p>{page["tagline"]}</p>' if page.get("tagline") else ""
            sections.append(
                f'<section class="page cover"><div class="brand">{esc(cfg["brand"])}</div>'
                f'<h1>{page["title"]}</h1><p class="subtitle">{page["subtitle"]}</p>'
                f"{image}{tagline}</section>")
        elif kind == "toc":
            items = "".join(f'<li><a href="#{slug(c["title"])}">{c["title"]}</a></li>'
                            for c in chapters)
            sections.append(f'<section class="page toc"><h2>Inside This Guide</h2>'
                            f"<ol>{items}</ol>{footer}</section>")
        else:
            body = "\n".join(block_html(b, cfg, images_dir) for b in page["blocks"])
            sections.append(f'<section class="page" id="{slug(page["title"])}">'
                            f'<h2>{page["title"]}</h2>{body}{footer}</section>')

    title = f'{cfg["brand"].title()} - {cfg["title"]}'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{CSS % cfg}</style>
</head>
<body>
<div class="book">
{chr(10).join(sections)}
</div>
</body>
</html>
"""


def write_pdf(html_path: Path, pdf_path: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit(
            "PDF export needs Playwright:\n"
            "    pip install playwright && playwright install chromium\n"
            "Or open the HTML in Chrome and use Print > Save as PDF "
            "(tick 'Background graphics').")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri())
        page.pdf(path=str(pdf_path), format="A4", print_background=True,
                 prefer_css_page_size=True)
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=HERE / "output",
                        help="output folder (default: ./output)")
    parser.add_argument("--open", action="store_true", help="open the HTML in your browser")
    parser.add_argument("--pdf", action="store_true", help="also export a PDF")
    parser.add_argument("--affiliate-url", help="override the affiliate link")
    args = parser.parse_args()

    cfg = dict(SETTINGS)
    if args.affiliate_url:
        cfg["affiliate_url"] = args.affiliate_url
    images_dir = HERE / cfg["images_dir"]

    args.out.mkdir(parents=True, exist_ok=True)
    html_path = args.out / f'{cfg["output_name"]}.html'
    html_path.write_text(build_html(cfg, PAGES, images_dir), encoding="utf-8")
    print(f"HTML: {html_path}")

    wanted = [b[1] for p in PAGES for b in p.get("blocks", []) if b[0] == "image"]
    wanted += [p["image"][0] for p in PAGES if p.get("image")]
    missing = [m for m in wanted if not (images_dir / m).is_file()]
    if missing:
        print(f"Using illustrations until these photos are added to {images_dir.name}/: "
              + ", ".join(missing))

    if args.pdf:
        pdf_path = html_path.with_suffix(".pdf")
        write_pdf(html_path, pdf_path)
        print(f"PDF:  {pdf_path}")
    if args.open:
        webbrowser.open(html_path.as_uri())


if __name__ == "__main__":
    main()
