# INESC API Python Project

### Install this project
`pip3 install -r requirements.txt`

### After project installed

run `make install` to configure install libs for this project and reload Systemd process

---

## Export Data
Há dois tipos de arquivos que podem ser criados ao exportar os dados: 

**.csv** e **.json**

Para essa exportação, você pode escolher algumas outras configurações:
  - collection
  - interval
  - between
  - path (obrigatório)

A ***collection*** serve para indicar de qual collection do banco de dados você quer buscar os dados.
Caso queira buscar todas, apenas não a utilize

O ***interval***, por padrão são **2** minutos. Essa propriedade define quantos minutos atrás da hora atual
você deseja de dados. Por exemplo, 5 minutos, então a consulta será feita dos registros contidos de 5 minutos atrás até agora. 
Caso queira buscar todos os registros, basta colocar esta propriedade como **0** (zero)

O ***between*** serve para definir qual o intervalo de tempo você quer os dados.
Por exemplo, precisamos buscar os dados de 01/03/2021 das 06h00 às 17h30, então passamos na propriedado: 
**2021-03-01-06:00:00 2021-03-01-17:30:00**

O ***path*** é um parâmetro obrigatório, é nele que você informará onde este(s) arquivo(s) serão salvos após sua criação.
Exemplo: **/home/usuario/exports**

### Exemplo de exportação:
Para este exemplo vamos usar um cenário teste de que precisamos dos dados da coleção **Robo** que tenham sido executados
no dia **02/03/2021 das 10h00 às 15h00** e que queremos esses dados exportados tanto em **csv**, quanto em **json**.

Para realizar esta exportação basta, no terminal digitar:

``python3 export.py --csv --json --collection=robo --between="2021-03-02-10:00:00 2021-03-02-15:00:00" 
--path=/home/myuser/exports``

Após o script finalizado, os arquivos estarão no diretório informado no **path**.
