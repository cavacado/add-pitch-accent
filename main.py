"""
    small pitch accent plugin for Anki
    draws svg of word and inserts it into the card
    @author     = cavacado
    @date         = 30/07/2020
    @version     = 0.01
"""
import traceback
import os
from . import draw_pitch, accent_dict


# Update note =================================================================
from anki.hooks import addHook
from aqt import mw
from aqt.qt import QKeySequence, QAction
from aqt.utils import showInfo

config = mw.addonManager.getConfig(__name__)

# Edit these field names if necessary =========================================
EXPRESSION_FIELD = config['expressionField']
DEFINITION_FIELD = config['definitionField']
HOT_KEY = config['hotKey']
# =============================================================================

# generate pitch accent svgs==========================
# environment
addon_path = os.path.dirname(__file__)
csv_path = os.path.join(addon_path, 'wadoku_pitchdb.csv')
acc_dict = accent_dict.get_accent_dict(csv_path)


def get_accent_pattern(field, corpus):
    try:
        return corpus.get(field, False)
    except Exception:
        showInfo("failed at getting accent pattern")
        traceback.print_exc()


def get_all_svg(assoc_list):
    if assoc_list:
        svgs = [draw_pitch.pitch_svg(word, pattern)
                for (word, pattern) in assoc_list]
        return "<br/>".join(svgs)
    else:
        return ""


def glossNote(f):
    if f[DEFINITION_FIELD]:
        return
    f[DEFINITION_FIELD] = get_all_svg(
        get_accent_pattern(f[EXPRESSION_FIELD], acc_dict))
    f.flush()


def setupMenu(ed):
    a = QAction('Regenerating pitch accent svgs', ed)
    if HOT_KEY:
        a.setShortcut(QKeySequence(HOT_KEY))
    a.triggered.connect(lambda: onRegenGlosses(ed))
    ed.form.menuEdit.addSeparator()
    ed.form.menuEdit.addAction(a)


def onRegenGlosses(ed):
    def callback():
        regenGlosses(ed, ed.selectedNotes())
        mw.reset()
    ed.editor.saveNow(callback)


def regenGlosses(ed, fids):
    mw.progress.start(max=len(fids), immediate=True)
    for (i, fid) in enumerate(fids):
        mw.progress.update(label='generating pitch accents...', value=i)
        f = mw.col.getNote(id=fid)
        try:
            glossNote(f)
        except Exception:
            print('definitions failed:')
            traceback.print_exc()
        try:
            f.flush()
        except Exception:
            raise Exception()
    mw.progress.finish()


addHook('browser.setupMenus', setupMenu)
