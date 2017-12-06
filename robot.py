from config import *
import wpilib
from wpilib import RobotDrive
class MyRobot(wpilib.IterativeRobot):
    '''Main robot class'''
    
    def robotInit(self):
        self.lr_motor           = wpilib.Spark(frontLeftChannel)
        self.rr_motor           = wpilib.Spark(rearLeftChannel)
        self.lf_motor           = wpilib.Spark(frontRightChannel)
        self.rf_motor           = wpilib.Spark(rearRightChannel)
        self.robot_drive        = wpilib.RobotDrive(self.lf_motor, self.lr_motor,
                                             self.rf_motor, self.rr_motor)
        self.robot_drive.setExpiration(Expiration)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontLeft, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearLeft, True)
        
        self.stick              = wpilib.Joystick(JoystickNum)
        self.gyro1              = wpilib.AnalogGyro(GyroNum)
        self.motorClimbOn       = wpilib.Spark(ClimbMotor)
        self.solenoid2          = wpilib.DoubleSolenoid(Solenoid2Num,SolenoidUselessNum)
        self.solenoid13         = wpilib.DoubleSolenoid(Solenoid1Num,Solenoid3Num)
        self.a                  = 0
        self.b                  = 0
    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
        self.a = 0
        self.b = 0
        self.solenoid13.set(1)
        self.solenoid2.set(1)
    def autonomousPeriodic(self):
        #move 65 inches
        if self.a < Time*40:
            self.robot_drive.mecanumDrive_Cartesian(0,0.7,0,self.gyro1.getRate());
            self.a = self.a + 1
        elif self.a < Time*40 + Wait*40:
        #solenoid
            self.solenoid13.set(2)
            self.solenoid2.set(0)
            self.a = self.a + 1
        else:
        #move backwards

            self.robot_drive.mecanumDrive_Cartesian(0,0,0,self.gyro1.getRate());
            if self.b < Time*40*50/165.1:
                self.robot_drive.mecanumDrive_Cartesian(0,-0.7,0,self.gyro1.getRate());
                self.b = self.b + 1
        
    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        self.robot_drive.mecanumDrive_Cartesian(0,0,0,self.gyro1.getRate());

        self.solenoid13.set(0)
        self.solenoid2.set(0)
    def disabledPeriodic(self):
        '''Called every 20ms in disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        self.a = 0
        self.solenoid2.set(1)
        self.solenoid13.set(1)
    def teleopPeriodic(self):
        '''Called every 20ms in teleoperated mode'''
        
        # Move a motor with a Joystick
        try:
            self.robot_drive.setSafetyEnabled(True)
            if self.isOperatorControl() and self.isEnabled():
                
                self.robot_drive.mecanumDrive_Cartesian(self.stick.getX(),
                                                       self.stick.getY(),
                                                       self.stick.getZ(), self.gyro1.getRate());

                if self.stick.getRawButton(1) == True: #climb
                    self.solenoid13.set(1)
                    self.solenoid2.set(1)
                if self.stick.getRawButton(2) == True: #climb
                    self.solenoid13.set(0)
                    self.solenoid2.set(0)

                if self.stick.getRawButton(3) == True:
                    self.sol = 2
                    self.solenoid13.set(self.sol)
                if self.stick.getRawButton(4) == True:
                    self.sol = 0
                    self.solenoid13.set(self.sol)

                


                if self.stick.getRawButton(5) == True: #climb
                    self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, self.gyro1.getRate())#set other motor to 0
                    self.motorClimbOn.set(ClimbEff)#start climbing
                if self.stick.getRawButton(6) == True: #climb
                    self.robot_drive.mecanumDrive_Cartesian(0, 0, 0, self.gyro1.getRate())#set other motor to 0
                    self.motorClimbOn.set(0)#start climbing
                wpilib.Timer.delay(0.005)
        except:
            raise error
if __name__ == '__main__':
    wpilib.run(MyRobot)
