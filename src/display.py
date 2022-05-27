''' A class to display the ballot information is defined in this module. '''


''' Imports '''
from typing import Any, Callable, Dict, List, Optional, Tuple
import sys
import re

from bokeh.io import output_file, show
from bokeh.layouts import column, row
from bokeh.models import Model, Range1d, Select, FixedTicker
from bokeh.plotting import Figure, curdoc, figure
from bokeh.transform import dodge, factor_cmap
from bokeh.document import Document

from CVRParser import Parser
from parsedData import ParsedData
from configInfo import ConfigInfo

# print to stderr
def log(*args, file=sys.stderr, **kwargs) -> None:
    print(*args, file=file, **kwargs)

###################################################################################################


''' A class for displaying ballot data '''

####
# use main guard when not using `bokeh serve`
if __name__ == '__main__':
    # output html file name
    output_file("CVR.html", mode='inline')
####

# model name
MODEL_NAME: str = 'Root'


def ballot_graph(batch_number: int,
                 ballot_number: int,
                 back_side=True) -> Model:
    '''
    Generate a ballot graph using the provided batch#, ballot# and side.
    '''

    # if ballot_number == 0, then it is a batch graph
    if ballot_number == 0:
        return batch_graph(batch_number)
    
    ballot = data.getBallot(batch_number, ballot_number)

    # map the office and party names
    map_parties = c.getParties()

    if back_side:
        dimensions = ballot.getBackBallotDimensions()
        df = ballot.getBack()
        map_offices = c.getBackOffices()
    else:
        dimensions = ballot.getFrontBallotDimensions()
        df = ballot.getFront()
        map_offices = c.getFrontOffices()

    #log('df', df, type(df), sep='\n---\n')
    #log('df.party', df.party, sep='\n---\n')
    #log('list(df.party)', list(df.party), sep='\n---\n')

    numColumns = dimensions[0]
    numRows = dimensions[1]
    c = ConfigInfo.getInstance()
    breakpoint = c.getBreak()


    # build up default mapping lists of numbers and letters
    parties = [chr(x) for x in range(65, numRows + 66)]
    offices = [str(x) for x in range(1, numColumns + 1)]

    if len(map_offices) > len(offices):
        map_offices = map_offices[:len(offices)]
    for index, item in enumerate(map_offices):
        office[index] = item
    if len(map_parties) > len(parties):
        map_parties = map_parties[:len(parties)]
    for index, item in enumerate(map_parties):
        parties[index] = item


    df["party"] = [parties[int(x)] for x in df.party]

    new_offices = []
    for x in df.office:
        y = int(x)
        if y > breakpoint:
            y -= breakpoint
        new_offices.append(offices[y - 1])
    df["office"] = new_offices
    # print(len(set(new_offices)))

    parties.append("")


    cmap = {
        "Vote"          : "#599d7A",
        "Questionable"  : "#f1d4Af",
        "None"          : "#f0f0f0"
    }

    TOOLTIPS = [
        ("Name", "@firstName" + " @lastName"),
        ("ID", "@id"),
        ("Party", "@party"),
        ("Office", "@office"),
        ("Vote", "@vote")
    ]


    ballot_figure = figure(title="State of Connecticut Official Ballot Data",
                           plot_width=len(offices) * c.getColumnWidth(),
                           plot_height=len(parties) * c.getRowHeight(),
                           x_range=offices,
                           y_range=list(reversed(parties)),
                           tools="hover",
                           toolbar_location=None,
                           tooltips=TOOLTIPS,
                           x_axis_location="above")

    r = ballot_figure.rect("office", "party",
                           0.95, 0.95,
                           source=df,
                           fill_alpha=0.6,
                           legend_field="vote",
                           color=factor_cmap(
                               'vote',
                               palette=list(cmap.values()),
                               factors=list(cmap.keys())))

    text_props = {"source": df, "text_align": "left", "text_baseline": "middle"}

    x = dodge("office", -0.45, range=ballot_figure.x_range)

    ballot_figure.text(x=x, y="party", text="firstName", text_font_size="13px", **text_props)

    ballot_figure.text(x=x, y=dodge("party", -0.2, range=ballot_figure.y_range),
                       text="lastName",
                       text_font_size="13px", **text_props)

    ballot_figure.text(x=x, y=dodge("party", 0.3, range=ballot_figure.y_range),
                       text="id", text_font_style="bold",
                       text_font_size="11px", **text_props)


    ballot_figure.xgrid.ticker = FixedTicker(ticks=[x for x in range(1, len(offices))])
    ballot_figure.ygrid.ticker = FixedTicker(ticks=[x for x in range(1, len(parties))])

    ballot_figure.outline_line_color = "black"
    ballot_figure.grid.grid_line_color = "black"
    ballot_figure.axis.axis_line_color = None
    ballot_figure.axis.major_tick_line_color = None
    ballot_figure.axis.major_label_standoff = 0
    ballot_figure.legend.orientation = "horizontal"
    ballot_figure.legend.location ="bottom_left"
    ballot_figure.hover.renderers = [r]

    return ballot_figure

def batch_graph(batch_number: int) -> Model:
    '''
    create a batch graph based on batch number
    '''

    vote_types: List[str] = ["Votes", "Questionable"]
    colors: List[str] = ["#718dbf", "#c9d9d3"]

    batch = data.getBatch(batch_number)

    graph_data: Dict[str, List[Any]] = {
        'candidate_names': list(batch.getCertainVotes().keys()),
        'Votes': list(batch.getCertainVotes().values()),
        'Questionable': list(batch.getUncertainVotes().values())
    }

    batch_figure: Figure = figure(x_range=list(batch.getCertainVotes().keys()),
                                  plot_height=600,
                                  plot_width=1000,
                                  title="Total Vote Count",
                                  toolbar_location=None,
                                  tools="hover",
                                  tooltips="$name @candidate_names: @$name")


    batch_figure.vbar_stack(vote_types,
                            x='candidate_names',
                            width=0.9,
                            color=colors,
                            source=graph_data,
                            legend_label=vote_types)

    batch_figure.y_range.start = 0
    batch_figure.yaxis.axis_label = "Votes"
    batch_figure.x_range.range_padding = 0.1
    batch_figure.xaxis.axis_label = "Candidates"
    batch_figure.xaxis.major_label_orientation = 1.2
    batch_figure.legend.location = "top_left"
    batch_figure.legend.orientation = "horizontal"
    batch_figure.y_range = Range1d(0, max(batch.getCertainVotes().values()) + 10)

    return batch_figure

def create_vote_result_layout(
        batch_number: int,
        ballot_number: int = 0,
        is_front: bool = True,
        *,
        batch_sel_reuse: Optional[Select] = None,
        ballot_sel_reuse: Optional[Select] = None,
        fb_sel_reuse: Optional[Select] = None,
        not_bokeh_serve: bool = False) -> Tuple[Model, Select, Select, Select]:
    '''
    display dropdown menus and graph of choice

    args:
        batch_number:
            Specify the batch # (starting from 1)
        ballot_number:
            Specify the ballot # (starting from 1)
            If ballot_number == 0, produce a batch summary graph instead
        is_front:
            Specify that the front side of the ballot is shown. Only useful when ballot_number != 0
        batch_sel_reuse:
            If not `None`, reuse an existing batch dropdown menu, which is returned from a
            previous call to `create_vote_result_graph`. Necessary for update callback. If `None`,
            a new dropdown menu is created.
        ballot_sel_reuse:
            If not `None`, reuse an existing ballot dropdown menu. Otherwise the menu is created.
        fb_sel_reuse:
            If not `None`, reuse an existing front-back dropdown menu. Otherwise the menu is created.

    return:
        [0]: the whole model to show.
        [1]: Batch dropdown menu (created or passthrough from argument).
        [2]: Ballot dropdown menu (created or passthrough from argument).
        [3]: Front-back dropdown menu (created or passthrough from argument).
    '''
    print(
        '[create_vote_result_graph] '
        f'batch_number = {batch_number}; '
        f'ballot_number = {ballot_number}; '
        f'is_front = {is_front}',
        file=sys.stderr)

    # they can take Tuple[str, str], str, but for uniformality we only supply tuple
    batch_list: List[Tuple[str, str]] = []
    ballot_list: List[Tuple[str, str]] = [('0', 'all')]

    for batch in range(1, len(data.getAllBatches()) + 1):
        batch_list.append(("Batch #" + str(batch), str(batch)))

    for ballot_index in range(1, len(data.getBatch(batch_number).getAllBallots()) + 1):
        ballot_list.append(("Ballot #" + str(ballot_index), str(ballot_index)))

    # only two items for front-back dropdown
    fb_list: List[Tuple[str, str]] = [("front", "front"), ("back", "back")]

    # create a batch graph if no ballot is specified;
    # otherwise create a ballot graph
    selected_figure: Model = ballot_graph(
        batch_number,
        ballot_number or 0,
        back_side = not is_front)

    batch_select: Select = batch_sel_reuse or Select(
        title='Batch Number',
        value=f'Batch #{batch_number}',
        options=batch_list)
    ballot_select: Select = ballot_sel_reuse or Select(
        title='Ballot Number',
        value=f'Ballot #{ballot_number}' if ballot_number > 0 else '0',
        options=ballot_list)
    fb_select: Select = fb_sel_reuse or Select(
        title='Front or Back',
        value='front' if is_front else 'back',
        options=fb_list)
    
    selection: Model = column(batch_select, ballot_select, fb_select, width=150)
    layout: Model = row(selection, selected_figure, name=MODEL_NAME)

    if not_bokeh_serve:
        show(layout)

    return layout, batch_select, ballot_select, fb_select


def _doc_replace_root(new_root: Model, old_name: str = MODEL_NAME) -> Model:
    '''
    remove the old root from doc, and then add the new root into the doc
    '''
    old_root: Model = curdoc().get_model_by_name(old_name)
    curdoc().remove_root(old_root)
    log(f'old_root = {(old_root, type(old_root))}')
    log(f'new_root = {(new_root, type(new_root))}')
    curdoc().add_root(new_root)
    return old_root


def _parse_int(name: str) -> int:
    # need to parse the numbers
    from re import compile as _c
    compiled = _c(r'.+#(\d+)$')  # match things like "words #1"
    try:
        return int(name)
    except ValueError:
        matched: Optional[re.Match[str]] = compiled.match(name)
        return int(matched.group(1)) if matched else 0


def register_dropdown(batch_sel: Select, ballot_sel: Select, fb_sel: Select) -> None:
    '''
    Register the dropdown callback for both dropdown menus

    batch_sel contains selections [ "all", "batch #1", ... ]
    ballot_sel contains selections [ "all", "ballot #1", ... ]
    fb_sel contains selections [ "front", "back" ]
    '''
    def bb_on_change(change_batch: bool) -> Callable[..., None]:
        '''
        Serve as the on_change function for batch_sel and ballot_sel

        change_batch: true for batch, false for ballot
        return: the callback function
        '''

        def func(attr: str, old: str, new: str) -> None:
            '''
            attr: changed attribute
            old: old value ("Batch #1", ...)
            new: new value
            '''
            log(f'{func}(attr={attr}, old={old}, new={new})')

            if attr != 'value' or old == new:
                return
            new_index: int = _parse_int(new)

            # get new indices
            batch_new: int = (new_index
                              if change_batch
                              else _parse_int(batch_sel.value))
            ballot_new: int = (new_index
                               if not change_batch
                               else _parse_int(ballot_sel.value))

            # replace root
            new_root: Model = create_vote_result_layout(
                batch_new,
                ballot_new,
                batch_sel_reuse=batch_sel,
                ballot_sel_reuse=ballot_sel,
                fb_sel_reuse=fb_sel)[0]
            _doc_replace_root(new_root, MODEL_NAME)

        return func

    def fb_on_change_func(attr: str, old: str, new: str) -> None:
        '''
        attr: changed attribute
        old: old value ("front" / "back")
        new: new value
        '''
        log(f'{fb_on_change_func}(attr={attr}, old={old}, new={new})')

        if attr != 'value' or old == new:
            return

        # replace root
        print(f'batch_sel = {batch_sel.value}', file=sys.stderr)
        print(f'ballot_sel = {ballot_sel.value}', file=sys.stderr)
        new_root: Model = create_vote_result_layout(
            _parse_int(batch_sel.value),
            _parse_int(ballot_sel.value),
            is_front = new == 'front',
            batch_sel_reuse=batch_sel,
            ballot_sel_reuse=ballot_sel,
            fb_sel_reuse=fb_sel)[0]
        _doc_replace_root(new_root, MODEL_NAME)


    batch_sel.on_change('value', bb_on_change(True))

    ballot_sel.on_change('value', bb_on_change(False))

    fb_sel.on_change('value', fb_on_change_func)

if __name__ == "__main__" or True:
    # we cannot use "main" guard when using `bokeh serve`
    # parse the CVR file and store the data
    p = Parser()
    data = ParsedData.getInstance()

    layout, batch_select, ballot_select, fb_select = create_vote_result_layout(1, 0)
    register_dropdown(batch_select, ballot_select, fb_select)
    curdoc().add_root(layout)

    # show(layout)
