# aedFaCT (automated expert discovery-based Fact-Checking Tool)

This repository includes the source codes of the aedFaCT Web browser extension presented in the paper titled "aedFaCT: Scientific Fact-Checking Made Easier via Semi-Automatic Discovery of Relevant Expert Opinions" accepted for the MEDIATE 2023 Workshop, co-located with ICWSM 2023.

## Prerequisites

````
Flask==2.2.2
Flask-Cors==3.0.10
newspaper3k==0.2.8
pybliometrics==3.3.0
spacy==3.5.0
stanfordcorenlp==3.9.1.1
````

## Steps for Deploying aedFaCT

- Download the source codes.
- Obtain a [Google Custom Search API key](https://developers.google.com/custom-search/v1/introduction), create the custom search engines, and update values in ````aedFaCT-server/server.py````.
- Install [Pybliometrics](https://pybliometrics.readthedocs.io/en/stable/index.html) and configure as [explained](https://pybliometrics.readthedocs.io/en/stable/configuration.html).
- Download "StanfordCoreNLP" and "elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5", from the repository of the [SIFRank+](https://github.com/sunyilgdx/SIFRank) algorithm and save them to ````aedFaCT-server/util/m_sifrank/````.
- Download [data.rar](https://drive.google.com/file/d/1jOMLpWzdXkbercs7q_Hp_cM8_jGHLjRN/view?usp=sharing) and extract to ````aedFaCT-server/util/````
- Deploy the server (````aedFaCT-server````) on localhost or a remote server and update server IP address and port number in ````aedFaCT-wbe/manifest.json```` and ````aedFaCT-wbe/background.js````.

## Citation

Please cite the following paper if you benefit from this repository in your research:
<!---
````
@inproceedings{altuncu2023,
  title={aedFaCT: Scientific Fact-Checking Made Easier via Semi-Automatic Discovery of Relevant Expert Opinions},
  authors={Altuncu, Enes and 
           Nurse, Jason~R.C. and 
           Bagriacik, Meryem and 
           Kaleba, Sophie and 
           Yuan, Haiyue and 
           Bonheme, Lisa and 
           Li, Shujun},
  year={2023},
  numpages={10},
  doi={},
  booktitle={Proceedings of the MEDIATE 2023 Workshop},
  publisher={Association for the Advancement of Artificial Intelligence},
}
````
--->
