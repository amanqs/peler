from .. import run_as_module

if not run_as_module:
    from ..exceptions import RunningAsFunctionLibError

    raise RunningAsFunctionLibError(
        "You are running 'Ayra' as a functions lib, not as run module. You can't access this folder.."
    )

from .. import *

DEVLIST = [
    719195224,  # @xditya
    1322549723,  # @danish_00
    1903729401,  # @its_buddhhu
    1054295664,  # @riizzvbss
    1924219811, # @Banned_3
    883761960,  # @SilenceSpe4ks
    910766621, # @thisrama
    1803618640, # @onlymeriz
    874946835,  # @vckyaz
    997461844, # @AyiinXd
    1784606556,  # @greyvbss
    844432220,  # @mrismanaziz
    2059198079, # @thekingofkazu
    951454060, # @riizzvbss
    993270486, # @deakajalah
    2003295492, #
    1191668125, # Rendy
    1488093812, # @ControlErrors
]

AYRA_IMAGES = [
    f"https://graph.org/file/{_}.jpg"
    for _ in [
        "a51b51ca8a7cc5327fd42",
        "02f9ca4617cec58377b9d",
    ]
]

stickers = [

]
