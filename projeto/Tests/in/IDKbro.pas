program ArrayFunGlobalTest;

var
    globalArr : array [1..5] of integer;
    globalSum, i : integer;

function SumGlobalArray : integer;
var
    i, total : integer;
begin
    total := 0;
    for i := 1 to 5 do
        total := total + globalArr[i];
    SumGlobalArray := total;
end;

function HelloWorld : string;
begin
    HelloWorld := 'Hello, World!';
end;

begin
    writeln('Digite 5 numeros:');
    
    for i := 1 to 5 do
        readln(globalArr[i]);

    globalSum := SumGlobalArray();
    
    writeln('Soma dos elementos: ', globalSum);
    writeln('Mensagem: ', HelloWorld());
    
    writeln('Elementos do array em ordem inversa:');
    for i := 5 downto 1 do
        writeln(globalArr[i]);
end.
