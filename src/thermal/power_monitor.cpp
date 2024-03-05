#include "power_monitor.hpp"
#include "booksim_config.hpp"

PowerMonitor::PowerMonitor(const Configuration &config, int inputs, int outputs) : inputs(inputs), outputs(outputs) {
  string pfile = config.GetStr("tech_file");
  PowerConfig pconfig;
  pconfig.ParseFile(pfile);

  channel_width = (double)config.GetInt("channel_width");

  numVC = (double)config.GetInt("num_vcs");
  depthVC  = (double)config.GetInt("vc_buf_size");

  //////////////////////////////////Constants/////////////////////////////
  //wire length in (mm)
  wire_length = pconfig.GetFloat("wire_length");
  //////////Metal Parameters////////////
  // Wire left/right coupling capacitance [ F/mm ]
  Cw_cpl = pconfig.GetFloat("Cw_cpl"); 
  // Wire up/down groudn capacitance      [ F/mm ]
  Cw_gnd = pconfig.GetFloat("Cw_gnd");
  Cw = 2.0 * Cw_cpl + 2.0 * Cw_gnd ;
  Rw = pconfig.GetFloat("Rw");
  // metal pitch [mm]
  MetalPitch = pconfig.GetFloat("MetalPitch"); 
  
  //////////Device Parameters////////////
  
  LAMBDA =  pconfig.GetFloat("LAMBDA")  ;       // [um/LAMBDA]
  Cd     =  pconfig.GetFloat("Cd");           // [F/um] (for Delay)
  Cg     =  pconfig.GetFloat("Cg");           // [F/um] (for Delay)
  Cgdl   =  pconfig.GetFloat("Cgdl");           // [F/um] (for Delay)
  
  Cd_pwr =  pconfig.GetFloat("Cd_pwr") ;           // [F/um] (for Power)
  Cg_pwr =  pconfig.GetFloat("Cg_pwr") ;           // [F/um] (for Power)
			       
  IoffN  = pconfig.GetFloat("IoffN");            // [A/um]
  IoffP  = pconfig.GetFloat("IoffP");            // [A/um]
  // Leakage from bitlines, two-port cell  [A]
  IoffSRAM = pconfig.GetFloat("IoffSRAM");  
  // [Ohm] ( D1=1um Inverter)
  R        = pconfig.GetFloat("R");                  
  // [F]   ( D1=1um Inverter - for Power )
  Ci_delay = (1.0 + 2.0) * ( Cg + Cgdl );   
  // [F]   ( D1=1um Inverter - for Power )
  Co_delay = (1.0 + 2.0) * Cd ;              


  Ci = (1.0 + 2.0) * Cg_pwr ;
  Co = (1.0 + 2.0) * Cd_pwr ;

  Vdd    = pconfig.GetFloat("Vdd");
  FO4    = R * ( 3.0 * Cd + 12 * Cg + 12 * Cgdl);		     
  tCLK   = 20 * FO4;
  fCLK   = 1.0 / tCLK;              

  H_INVD2=(double)pconfig.GetInt("H_INVD2");
  W_INVD2=(double)pconfig.GetInt("W_INVD2") ;
  H_DFQD1=(double)pconfig.GetInt("H_DFQD1");
  W_DFQD1= (double)pconfig.GetInt("W_DFQD1");
  H_ND2D1= (double)pconfig.GetInt("H_ND2D1");
  W_ND2D1=(double)pconfig.GetInt("W_ND2D1");
  H_SRAM=(double)pconfig.GetInt("H_SRAM");
  W_SRAM=(double)pconfig.GetInt("W_SRAM");

  ChannelPitch = 2.0 * MetalPitch ;
  CrossbarPitch = 2.0 * MetalPitch ;

  _switchPowerLeak = 0.0;
  _switchPower = 0.0;
  _switchCtrlPower = 0.0;
  _recentPowerUsage = 0.0;
  _cycleCount = 0;
}

PowerMonitor::~PowerMonitor() {}

double PowerMonitor::powerCrossbar(double width, double from, double to) const {
  // datapath traversal power
  double Wxbar = width * outputs * CrossbarPitch ;
  double Hxbar = width * inputs  * CrossbarPitch ;

  // wires
  double CwIn  = Wxbar * Cw ;
  double CwOut = Hxbar * Cw ;

  // cross-points
  double Cxi = (1.0/16.0) * CwOut ;
  double Cxo = 4.0 * Cxi * (Co_delay/Ci_delay) ;

  // drivers
  double Cti = (1.0/16.0) * CwIn ;
  double Cto = 4.0 * Cti * (Co_delay/Ci_delay) ;

  double CinputDriver = 5.0/16.0 * (1 + Co_delay/Ci_delay) * (0.5 * Cw * Wxbar + Cti) ;

  // total switched capacitance
  
  //this maybe missing +Cto
  double Cin  = CinputDriver + CwIn + Cti + (outputs * Cxi) ;
  if ( to < outputs/2 ) {
    Cin -= ( 0.5 * CwIn + outputs/2 * Cxi) ;
  }
  //this maybe missing +cti
  double Cout = CwOut + Cto + (inputs * Cxo) ;
  if ( from < inputs/2) {
    Cout -= ( 0.5 * CwOut + (inputs/2 * Cxo)) ;
  }
  return 0.5 * (Cin + Cout) * (Vdd * Vdd * fCLK) ;
}

double PowerMonitor::powerCrossbarCtrl(double width) const {
  // datapath traversal power
  double Wxbar = width * outputs * CrossbarPitch ;
  double Hxbar = width * inputs  * CrossbarPitch ;

  // wires
  double CwIn  = Wxbar * Cw ;

  // drivers
  double Cti  = (5.0/16.0) * CwIn ;

  // need some estimate of how many control wires are required
  double Cctrl  = width * Cti + (Wxbar + Hxbar) * Cw  ; 
  double Cdrive = (5.0/16.0) * (1 + Co_delay/Ci_delay) * Cctrl ;

  return (Cdrive + Cctrl) * (Vdd*Vdd) * fCLK ;
}

double PowerMonitor::powerCrossbarLeak(double width) const {
  // datapath traversal power
    double Wxbar = width * outputs * CrossbarPitch ;
    double Hxbar = width * inputs  * CrossbarPitch ;

    // wires
    double CwIn  = Wxbar * Cw ;
    double CwOut = Hxbar * Cw ;
    // cross-points
    double Cxi = (1.0/16.0) * CwOut ;
    // drivers
    double Cti  = (1.0/16.0) * CwIn ;

    return 0.5 * (IoffN + 2 * IoffP)*width*(inputs*outputs*Cxi+inputs*Cti+outputs*Cti)/Ci;
}

void PowerMonitor::CrossbarTraversal(int input, int output) {
    _switchPowerLeak += powerCrossbarLeak(channel_width);
    double Px = powerCrossbar(channel_width, input, output);
	_switchPower += channel_width * Px;
	_switchCtrlPower += powerCrossbarCtrl(channel_width);
}

void PowerMonitor::Step() {
    double power_usage = _switchPowerLeak + _switchPower + _switchCtrlPower;
    _power_trace.push_back(power_usage);
    _recentPowerUsage += power_usage;
    if (_cycleCount >= 100) {
        _recentPowerUsage -= _power_trace[_cycleCount - 100];
    }

    _cycleCount++;
    _switchPowerLeak = 0.0;
    _switchPower = 0.0;
    _switchCtrlPower = 0.0;
}

double PowerMonitor::GetRecentPowerUsage() const {
    return _recentPowerUsage / 100;
}
