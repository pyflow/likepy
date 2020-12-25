
# Grammar

```
File = {Statement | newline} eof .

Statement = DefStmt | IfStmt | ForStmt | SimpleStmt .

DefStmt = 'def' identifier '(' [Parameters [',']] ')' ':' Suite .

Parameters = Parameter {',' Parameter}.

Parameter = identifier | identifier '=' Test | '*' identifier | '**' identifier .

IfStmt = 'if' Test ':' Suite {'elif' Test ':' Suite} ['else' ':' Suite] .

ForStmt = 'for' LoopVariables 'in' Expression ':' Suite .

Suite = [newline indent {Statement} outdent] | SimpleStmt .

SimpleStmt = SmallStmt {';' SmallStmt} [';'] '\n' .
# NOTE: '\n' optional at EOF

SmallStmt = ReturnStmt
          | BreakStmt | ContinueStmt | PassStmt
          | AssignStmt
          | ExprStmt
          | LoadStmt
          .

ReturnStmt   = 'return' [Expression] .
BreakStmt    = 'break' .
ContinueStmt = 'continue' .
PassStmt     = 'pass' .
AssignStmt   = Expression ('=' | '+=' | '-=' | '*=' | '/=' | '//=' | '%=' | '&=' | '|=' | '^=' | '<<=' | '>>=') Expression .
ExprStmt     = Expression .

LoadStmt = 'load' '(' string {',' [identifier '='] string} [','] ')' .

Test = IfExpr | PrimaryExpr | UnaryExpr | BinaryExpr | LambdaExpr .

IfExpr = Test 'if' Test 'else' Test .

PrimaryExpr = Operand
            | PrimaryExpr DotSuffix
            | PrimaryExpr CallSuffix
            | PrimaryExpr SliceSuffix
            .

Operand = identifier
        | int | float | string
        | ListExpr | ListComp
        | DictExpr | DictComp
        | '(' [Expression [',']] ')'
        .

DotSuffix   = '.' identifier .
SliceSuffix = '[' [Expression] [':' Test [':' Test]] ']' .
CallSuffix  = '(' [Arguments [',']] ')' .

Arguments = Argument {',' Argument} .
Argument  = Test | identifier '=' Test | '*' Test | '**' Test .

ListExpr = '[' [Expression [',']] ']' .
ListComp = '[' Test {CompClause} ']'.

DictExpr = '{' [Entries [',']] '}' .
DictComp = '{' Entry {CompClause} '}' .
Entries  = Entry {',' Entry} .
Entry    = Test ':' Test .

CompClause = 'for' LoopVariables 'in' Test | 'if' Test .

UnaryExpr = '+' Test
          | '-' Test
          | '~' Test
          | 'not' Test
          .

BinaryExpr = Test {Binop Test} .

Binop = 'or'
      | 'and'
      | '==' | '!=' | '<' | '>' | '<=' | '>=' | 'in' | 'not' 'in'
      | '|'
      | '^'
      | '&'
      | '<<' | '>>'
      | '-' | '+'
      | '*' | '%' | '/' | '//'
      .

LambdaExpr = 'lambda' [Parameters] ':' Test .

Expression = Test {',' Test} .
# NOTE: trailing comma permitted only when within [...] or (...).

LoopVariables = PrimaryExpr {',' PrimaryExpr} .
```