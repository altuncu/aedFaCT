# aedFaCT (automated expert discovery-based Fact-Checking Tool)
Source codes of the aedFaCT Web browser extension presented in the paper titled "aedFaCT: Scientific Fact-Checking Made Easier via Semi-Automatic Discovery of Relevant Expert Opinions".




- Download StanfordCoreNLP and elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5 to m_sifrank folder
- Install Pybliometrics and configure as explained here: https://pybliometrics.readthedocs.io/en/stable/configuration.html
- Obtain Google API key and update values in server.py
- Deploy Flask server and update values in manifest.json and background.js with server IP address and port number
- Download data.rar from https://drive.google.com/file/d/1jOMLpWzdXkbercs7q_Hp_cM8_jGHLjRN/view?usp=sharing and extract to server/util/
