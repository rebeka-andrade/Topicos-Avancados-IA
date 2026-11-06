package ifpe2026;

import robocode.*;
import robocode.util.Utils;
import java.awt.Color;

/** Robo circular com radar de varredura e mira simples. */
public class Rebeka extends Robot {
    private int direcao = 1;
    private int tirosRecebidos = 0;

    public void run() {
        setBodyColor(new Color(25, 70, 150));
        setGunColor(Color.ORANGE);
        setRadarColor(Color.CYAN);
        setBulletColor(Color.YELLOW);
        setScanColor(Color.GREEN);

        // Mantem o canhao e o radar independentes do corpo.
        setAdjustGunForRobotTurn(true);
        setAdjustRadarForGunTurn(true);
        setAdjustRadarForRobotTurn(true);

        while (true) {
            // Movimento circular no estilo SpinBot.
            turnRight(30 * direcao);
            ahead(85 * direcao);

            // Procura qualquer robo; nao trava em um alvo.
            turnRadarRight(360);
        }
    }

    public void onScannedRobot(ScannedRobotEvent evento) {
        double distancia = evento.getDistance();
        // Direcao absoluta do inimigo, medida em graus.
        double direcaoAlvo = getHeading() + evento.getBearing();
        double giroCanhao = Utils.normalRelativeAngleDegrees(
            direcaoAlvo - getGunHeading()
        );

        // Mira antes de disparar. O radar nao persegue o alvo.
        turnGunRight(giroCanhao);

        double potencia;
        if (distancia < 130 && getEnergy() > 35) {
            potencia = 3.0;
        } else if (distancia < 350 && getEnergy() > 15) {
            potencia = 1.8;
        } else {
            potencia = 0.7;
        }

        if (getEnergy() > potencia + 1 && getGunHeat() == 0) {
            fire(potencia);
        }
    }

    public void onHitByBullet(HitByBulletEvent evento) {
        tirosRecebidos++;
        direcao = -direcao;
        turnRight(45 * direcao);
        ahead(110 * direcao);
        if (tirosRecebidos % 3 == 0) {
            turnRight(90);
        }
    }

    public void onHitWall(HitWallEvent evento) {
        direcao = -direcao;
        back(90);
        turnRight(75);
    }

    public void onHitRobot(HitRobotEvent evento) {
        direcao = -direcao;
        back(75);
        turnRight(60);
    }
}



