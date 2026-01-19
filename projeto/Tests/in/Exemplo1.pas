program Exemplo1;

var
    a : array[1..3] of integer;
    s : string;
    i : integer;
    r : real;

begin
    s := 'Value: ';
    i := 2;
    r := (i + 3) * 2.5;

    a[i] := length(s) + i;
    a[i + 1] := a[i] * 2;

    writeln(s + 'ok');
    writeln(r);
    writeln(a[2]);
    writeln(a[3]);
end.
