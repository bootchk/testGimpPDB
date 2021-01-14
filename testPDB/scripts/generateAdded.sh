# generateAdded.sh
comm -13 pdb2_10.dump.signatures  pdb2_99.dump.signatures | gawk '{ print $1}' > addedOrSignatureChanged
comm -23 addedOrSignatureChanged signatureChanged > added
