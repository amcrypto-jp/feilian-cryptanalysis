function Header(h)
  if FORMAT:match('latex') then
    if pandoc.utils.stringify(h.content) == 'Assessment and scope' then
      return {pandoc.RawBlock('latex', '\\clearpage'), h}
    end
    return {pandoc.RawBlock('latex', '\\Needspace{5\\baselineskip}'), h}
  end
end

function Table(t)
  local n = #t.colspecs
  local first_header = t.head.rows[1] and pandoc.utils.stringify(t.head.rows[1].cells[1].contents) or ''
  if n == 4 and first_header == 'Variant' then
    t.colspecs = {{pandoc.AlignLeft, .22}, {pandoc.AlignRight, .19},
                 {pandoc.AlignLeft, .29}, {pandoc.AlignLeft, .30}}
  elseif n == 4 then
    t.colspecs = {{pandoc.AlignLeft, .07}, {pandoc.AlignLeft, .31},
                 {pandoc.AlignLeft, .31}, {pandoc.AlignLeft, .31}}
  elseif n == 3 then
    t.colspecs = {{pandoc.AlignLeft, .22}, {pandoc.AlignLeft, .39}, {pandoc.AlignLeft, .39}}
  elseif n == 2 then
    t.colspecs = {{pandoc.AlignLeft, .43}, {pandoc.AlignLeft, .57}}
  elseif n == 5 then
    t.colspecs = {{pandoc.AlignRight, .12}, {pandoc.AlignRight, .22}, {pandoc.AlignRight, .22},
                 {pandoc.AlignRight, .22}, {pandoc.AlignRight, .22}}
  end
  if FORMAT:match('latex') then
    return {pandoc.RawBlock('latex', '\\Needspace{7\\baselineskip}'), t}
  end
  if FORMAT:match('html') then
    return pandoc.Div({t}, pandoc.Attr('', {'table-scroll'}, {role='region', tabindex='0', ['aria-label']='Comparison table'}))
  end
  return t
end

-- Long digests and identifiers are prose evidence, not unbreakable code blocks.
function Code(c)
  if FORMAT:match('latex') and #c.text > 28 and not c.text:find('[{}\\]') then
    local escaped = c.text:gsub('%%', '\\%%'):gsub('#', '\\#')
    return pandoc.RawInline('latex', '\\nolinkurl{' .. escaped .. '}')
  end
end
