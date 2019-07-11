# This file contains code for reformatting the Virus-Host DB's data into a more workable format. It's quite long, so
# I thought it best to separate it from the rest of the code.

import csv
#from utils import *


__all__ = ['VHDBEntry', 'getListOfEntries', 'Virus', 'Host', 'Sourcing', 'HostSource', 'MyVHDB', 'MyVHDBEntry']

class VHDBEntry:
    def __init__(self, field_list):
        self.virus_tax_id    = field_list[0]
        self.virus_name      = field_list[1]
        self.virus_lineage   = field_list[2]
        self.refseq_id       = field_list[3]
        self.KEGG_GENOME     = field_list[4]
        self.KEGG_DISEASE    = field_list[5]
        self.DISEASE         = field_list[6]
        self.host_tax_id     = field_list[7]
        self.host_name       = field_list[8]
        self.host_lineage    = field_list[9]
        self.pmid            = field_list[10]
        self.evidence        = field_list[11]
        self.sample_type     = field_list[12]
        self.source_organism = field_list[13]

    def __str__(self):
        return """
Entry:
    virus tax id:    %s
    virus name:      %s
    virus lineage:   %s
    refseq_id:       %s
    KEGG GENOME:     %s
    KEGG DISEASE:    %s
    DISEASE:         %s
    host tax id:     %s
    host name:       %s
    host lineage:    %s
    pmid:            %s
    evidence:        %s
    sample_type:     %s
    source_organism: %s
        """ % (self.virus_tax_id, self.virus_name, self.virus_lineage, self.refseq_id,
               self.KEGG_GENOME, self.KEGG_DISEASE, self.DISEASE, self.host_tax_id, self.host_name,
               self.host_lineage, self.pmid, self.evidence, self.sample_type, self.source_organism)

def getListOfEntries(infile):
    entries = []
    with open(infile) as tsv:
        for line in csv.reader(tsv, delimiter="\t"):
            if line[7] == '':
                continue
            new_entry = VHDBEntry(line)
            entries.append(new_entry)

    return entries

class Virus:
    def __init__(self, virus_tax_id, virus_name, virus_lineage, refseq_id, KEGG_GENOME, KEGG_DISEASE,
                       DISEASE):
        self.tax_id       = virus_tax_id
        self.name         = virus_name
        self.lineage      = virus_lineage
        self.refseq_id    = refseq_id
        self.KEGG_GENOME  = KEGG_GENOME
        self.KEGG_DISEASE = KEGG_DISEASE
        self.DISEASE      = DISEASE

    @classmethod
    def fromVHDBEntry(cls, vhdbentry):
        return cls(vhdbentry.virus_tax_id, vhdbentry.virus_name, vhdbentry.virus_lineage, vhdbentry.refseq_id, vhdbentry.KEGG_GENOME, vhdbentry.KEGG_DISEASE, vhdbentry.DISEASE)

    def __str__(self):
        return """Virus:
    tax id:       %s
    name:         %s
    lineage:      %s
    refseq id:    %s
    KEGG_GENOME:  %s
    KEGG_DISEASE: %s
    DISEASE:      %s""" % (self.tax_id, self.name, self.lineage, self.refseq_id, self.KEGG_GENOME, self.KEGG_DISEASE, self.DISEASE)

class Host:
    def __init__(self, host_tax_id, host_name, host_lineage):
        self.tax_id  = host_tax_id
        self.name    = host_name
        self.lineage = host_lineage

    @classmethod
    def fromVHDBEntry(cls, vhdbentry):
        return cls(vhdbentry.host_tax_id, vhdbentry.host_name, vhdbentry.host_lineage)

    def __str__(self):
        return """Host:
    tax id:  %s
    name:    %s
    lineage: %s""" % (self.tax_id, self.name, self.lineage)

class Sourcing:
    def __init__(self, pmid, evidence, sample_type, source_organism):
        self.pmid            = pmid
        self.evidence        = evidence
        self.sample_type     = sample_type
        self.source_organism = source_organism

    def __str__(self):
        return """Sourcing:
    pmid:            %s
    evidence:        %s
    sample type:     %s
    source organism: %s"""

class HostSource:
    def __init__(self, host, source):
        self.host   = host
        self.source = source

    def __str__(self):
        return "%s\n%s" % (self.host, self.source)
            

# One-to-many relation of viruses to hosts, instead of one-to-one
class MyVHDB:
    def __init__(self, virus_host_dict):
        self.virus_host_dict = virus_host_dict
    
    @classmethod
    def fromVHDBEntries(cls, vhdbentries):
        virus_host_dict = {}
        for entry in vhdbentries:
            virus = Virus.fromVHDBEntry(entry)
            host  = Host.fromVHDBEntry(entry)
            if virus.tax_id in virus_host_dict:
                virus_host_dict[virus.tax_id].addHost(host)
            else:
                virus_host_dict[virus.tax_id] = MyVHDBEntry(virus, [host])
        return cls(virus_host_dict)

    def __getitem__(self, key):
        return self.virus_host_dict[key]

    def keys(self):
        return self.virus_host_dict.keys()

    def items(self):
        return self.virus_host_dict.items()

    def __str__(self):
        return self.virus_host_dict.__str__()


class MyVHDBEntry:
    def __init__(self, virus, hosts):
        self.virus = virus
        self.hosts = hosts

    def addHost(self, host):
        self.hosts.append(host)

    def __str__(self):
        virus_string = "\tVirus Data:\n\t\ttax_id: %s\n\t\tname: %s\n\t\tlineage: %s\n\t\trefseq_id: %s\n\t\tKEGG_GENOME: %s\n\t\tKEGG_DISEASE: %s\n\t\tDISEASE: %s" %\
            (self.virus.tax_id, self.virus.name, self.virus.lineage, self.virus.refseq_id, self.virus.KEGG_GENOME, self.virus.KEGG_DISEASE, self.virus.DISEASE)
        host_strings = ""
        for host in self.hosts:
            host_string = "\tHost Data:\n\t\ttax_id: %s\n\t\tname: %s\n\t\tlineage: %s\n" %\
                (host.tax_id, host.name, host.lineage)
            host_strings = "%s%s" % (host_strings, host_string)
        return "Virus %s:\n%s\n%s" % (self.virus.tax_id, virus_string, host_strings)

    def __repr__(self):
        return self.__str__()
    
# Name records sometimes abbreviate the genus name (e.g. "A. mellifera") and sometimes contain multiple species in the format "speciesA x speciesB x ...".
# This method extracts all names and possible abbreviations for them.
def getSpeciesNamesFromNameRecord(name):
    species_names = name.split(" x ")
    orig_length = len(species_names)
    for species_name in species_names[:orig_length]:
        split_name = species_name.split(' ')
        abbrev_genus = "{}.".format(split_name[0][0])
        for n in split_name[1:]:
            abbrev_genus = "{} {}".format(abbrev_genus, n)
            
        species_names.append(abbrev_genus)
    
    return species_names
        
        
        
    
if __name__ == '__main__':
    print("Hi!")
    print(getSpeciesNamesFromNameRecord("GenusA speciesA x GenusB speciesB"))