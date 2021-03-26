topics = [
    'topic_sala/sensor/temperatura', 'topic_sala/sensor/umidade', 'topic_sala/sensor/iluminacao',
    'topic_sala/config/frequencia', 'topic_sala/config/habilitar', 'topic_sala/Alarme/habilitar',

    'topic_Armaz/sensor/temperatura', 'topic_Armaz/sensor/umidade', 'topic_Armaz/sensor/iluminacao',
    'topic_Armaz/config/frequencia', 'topic_Armaz/config/habilitar', 'topic_Armaz/Alarme/habilitar',

    'topic_Imp3D/sensor/temperatura', 'topic_Imp3D/sensor/umidade', 'topic_Imp3D/sensor/iluminacao',
    'topic_Imp3D/config/frequencia', 'topic_Imp3D/config/habilitar', 'topic_Imp3D/Alarme/habilitar',
    'topic_Imp3D/impressao/atual', 'topic_Imp3D/impressao/tamanho', 'topic_Imp3D/arquivo', 'topic_Imp3D/status',
    'topic_Imp3D/tempo/total', 'topic_Imp3D/tempo/restante', 'topic_Imp3D/sensor/temp_extrude',
    'topic_Imp3D/sensor/temp_bed',

    'topic_Arm/sensor/posX', 'topic_Arm/sensor/posY', 'topic_Arm/sensor/posZ', 'topic_Arm/sensor/joint1',
    'topic_Arm/sensor/joint2', 'topic_Arm/sensor/joint3', 'topic_Arm/sensor/joint4',
    'topic_Arm/sensor/joint5', 'topic_Arm/sensor/joint6', 'topic_Arm/sensor/joint7',
    'topic_Arm/sensor/velocidade', 'topic_Arm/sensor/joints',
    'topic_Arm/sensor/vel1', 'topic_Arm/sensor/vel2', 'topic_Arm/sensor/vel3', 'topic_Arm/sensor/vel4',
    'topic_Arm/sensor/vel5', 'topic_Arm/sensor/vel6', 'topic_Arm/sensor/vel7',
    'topic_Arm/sensor/garra', 'topic_Arm/sensor/comando',

    'topic_Barr/config/frequencia', 'topic_Barr/config/habilitar', 'topic_Barr/alarme/habilitar',
    'topic_Barr/sensor/Barreira1', 'topic_Barr/sensor/Barreira2', 'topic_Barr/sensor/Barreira3',
    'topic_Barr/sensor/Barreira4',

    'topic_Alarmes/erro/Sala/temp', 'topic_Alarmes/erro/Sala/umid',
    'topic_Alarmes/erro/Imp3D/temp', 'topic_Alarmes/erro/Imp3D/umid', 'topic_Alarmes/erro/Imp3D/extr',
    'topic_Alarmes/erro/Imp3D/mesa', 'topic_Alarmes/erro/Imp3D/impressora', 'topic_Alarmes/erro/Armaz/temp',
    'topic_Alarmes/erro/Armaz/umid', 'topic_Alarmes/erro/erro_impres', 'topic_Alarmes/erro/temp_mesa',
    'topic_Alarmes/erro/Robo', 'topic_Alarmes/erro/Garra', 'topic_Alarmes/erro/Barreiras/b1',
    'topic_Alarmes/erro/Barreiras/b2', 'topic_Alarmes/erro/Barreiras/b3', 'topic_Alarmes/erro/Barreiras/b4'

                                                                          'topic_Geral/dados/nome',
    'topic_Geral/dados/data', 'topic_Geral/dados/hora', 'topic_Geral/dados/periodo',
    'topic_Geral/dados/ilha', 'topic_Geral/dados/idProjeto', 'topic_Geral/dados/idTeste',
    'topic_Geral/controle/ini_rec', 'topic_Geral/controle/fim_rec'

]

topics_collections = {
    'sala': 'sala',
    'Imp3D': 'imp3D',
    'Armaz': 'armaz',
    'Arm': 'robo',
    'Alarmes': 'alarmes',
    'Barr': 'barreiras',
    'Geral': 'geral'
}

topic_by_values = {
    'topic_Arm/sensor/': ['posX', 'posY', 'posZ', 'joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7',
                          'vel1', 'vel2', 'vel3', 'vel4', 'vel5', 'vel6', 'vel7'],
    'topic_Alarmes/erro/Robo': ['alarmHigh'],
}
