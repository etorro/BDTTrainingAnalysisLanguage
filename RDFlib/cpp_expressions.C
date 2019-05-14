void plotHT() {
    ROOT::EnableImplicitMT();
    ROOT::RDataFrame df("recoTree", "data16_00311402_example.root");
    auto h = df.Histo1D({"", ";HT [GeV];# entries", 100, 0, 2000}, "event_HT");

    TCanvas c;
    h->Draw();
    c.SaveAs("HT.pdf");
}


void plotTrackpT() {
    ROOT::EnableImplicitMT();
    ROOT::RDataFrame df("recoTree", "data16_00311402_example.root");
    auto h = df.Histo1D({"", ";Track p_{T} [GeV];# entries", 100, 0, 20}, "Track_pT");

    TCanvas c;
    h->Draw();
    c.SaveAs("trackpt.pdf");
}


void plotTrackpTcuts() {
    ROOT::EnableImplicitMT();
    ROOT::RDataFrame df("recoTree", "data16_00311402_example.root");

    auto h = df.Define("goodTrack_pt2", "Track_pT[Track_pT > 2.0]")
      .Histo1D({"", ";Track p_{T} [GeV];# entries", 100, 0, 20}, "goodTrack_pt2");

    auto heta = df.Define("goodTrack_pt2eta", "Track_pT[Track_pT > 3.0 && abs(Track_eta)<1.0]")
               .Histo1D({"", ";Track p_{T} [GeV];# entries", 100, 0, 20}, "goodTrack_pt2eta");

    TCanvas c;
    h->Draw();
    heta->Draw("same");
    c.SaveAs("trackpt2.pdf");
}


void plotHT_Jetcuts() {
    ROOT::EnableImplicitMT();
    ROOT::RDataFrame df("recoTree", "data16_00311402_example.root");
    auto h1 = df.Histo1D({"", ";HT [GeV];# entries", 100, 0, 2000}, "event_HT");

    auto h = df.Filter("Sum(CalibJet_pT > 40 && abs(CalibJet_eta) < 1.0) > 1", "More than one jet with pt > 40 and abs(eta) < 1.0")
               .Histo1D({"", ";HT [GeV];# entries", 100, 0, 2000}, "event_HT");

    TCanvas c;
    h1->Draw();
    h->Draw("same");
    c.SaveAs("HT_2jets.pdf");
}



// add cpp expression in RDF Define
template <typename T> using Vec = const ROOT::RVec<T>&;
using FourVector = ROOT::Math::PtEtaPhiMVector;

  double wrapPhi(double phi){
    static const double M_2PI = 2*M_PI;
    while (phi> M_PI) phi -= M_2PI;
    while (phi<-M_PI) phi += M_2PI;
    return phi;

  };

  double DeltaPhi(double phi1, double phi2){
    double delPhi = wrapPhi(phi1-phi2);
    return fabs(delPhi);
  };

  double DeltaR(double phi1, double phi2, double eta1, double eta2){
    double delPhi = wrapPhi(phi1-phi2);
    double delEta = eta1-eta2;

    return(sqrt(delPhi*delPhi+delEta*delEta));
  };

auto DeltaR2(double phi1, double phi2, double eta1, double eta2){
    double delPhi = wrapPhi(phi1-phi2);
    double delEta = eta1-eta2;

    return(delPhi*delPhi+delEta*delEta);
  };

auto compute_mindRpt(Vec<double> eta1, Vec<double> phi1, Vec<double> eta2, Vec<double> phi2, Vec<double> pt2)
{
  ROOT::RVec<double> mindRvec;
  double mindR=99;
  for (auto i = 0; i < eta1.size(); i++) {
    for (auto j = 0; j < eta2.size(); j++) {    
      if(pt2[j]>2){
	auto dR = DeltaR2(phi1[i], phi2[j], eta1[i], eta2[j]);
	if(dR<mindR) mindR=dR;
      }
    }
    mindRvec.push_back(sqrt(mindR));
  }
  return mindRvec;

};


void plotdRjetTrackpt() {
    ROOT::EnableImplicitMT();
    ROOT::RDataFrame df("recoTree", "data16_00311402_example.root");
    auto h = df.Filter("Sum(CalibJet_pT > 40 && abs(CalibJet_eta) < 2.5) >= 2", "At least two jets")
      .Define("mindR", compute_mindRpt, {"CalibJet_eta", "CalibJet_phi", "Track_eta", "Track_phi", "Track_pT"})
               .Histo1D({"", ";mindR ;# entries", 100, 0, 1}, "mindR");

    TCanvas c;
    h->Draw();
    c.SaveAs("mindR.pdf");
}

