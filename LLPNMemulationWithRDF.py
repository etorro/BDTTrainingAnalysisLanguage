import ROOT
RDF = ROOT.ROOT.RDataFrame

d   = RDF("recoTree","LLPRO_study_125_35.root")


d = d.Define("numEm","Sum(L1_emRoI_E>-10)")
d = d.Filter("numEm>0")
d = d.Filter("Sum(L1_tauRoI_E>30)>0")
d = d.Define("leadTau","L1_tauRoI_E[0]")
d = d.Define("mindRtauEm","double mind=1000; \
        vector<double> mdR; \
        for(int i=0; i<L1_tauRoI_eta.size();i++){ \
            mind=1000; \
            for(int j=0; j<L1_emRoI_eta.size();j++) { \
                double deta = L1_tauRoI_eta[i]-L1_emRoI_eta[j]; \
                double dphi = L1_tauRoI_phi[i]-L1_emRoI_phi[j]; \
                if(dphi>M_PI) dphi -= 2*M_PI;\
                else if(dphi<-M_PI) dphi += 2*M_PI;\
                double r2=deta*deta+dphi*dphi; \
                if(r2<mind){mind=r2;\
                }\
            } \
            mdR.push_back(sqrt(mind));\
            } \
        return mdR;"\
    )
  
d = d.Define("matchIndextauEm","double mind=1000;  int index=-1;\
        vector<int> em_index; \
            for(int i=0; i<L1_tauRoI_eta.size();i++){ \
                mind=1000; index=-1;\
                for(int j=0; j<L1_emRoI_eta.size();j++) { \
                    double r2=(L1_tauRoI_eta[i]-L1_emRoI_eta[j])*(L1_tauRoI_eta[i]-L1_emRoI_eta[j])+(L1_tauRoI_phi[i]-L1_emRoI_phi[j])*(L1_tauRoI_phi[i]-L1_emRoI_phi[j]); \
                   if(r2<mind){mind=r2;index =j;\
                    }\
                } \
            em_index.push_back(index);\
            } \
        return em_index;"\
    )
d = d.Define("tauEMF","vector<double> emf;\
    for(int i=0; i<L1_tauRoI_eta.size();i++){ \
        emf.push_back(L1_emRoI_E[matchIndextauEm[i]]/L1_tauRoI_E[i]);\
    }\
    return emf;"
        )    
d = d.Define("passLLPNM","mindRtauEm[0]>0.01 && L1_tauRoI_E[0]>30")

d.Snapshot("recoTree", "testLLP1.root")
