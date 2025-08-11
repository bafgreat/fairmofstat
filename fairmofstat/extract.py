from fairmofstat import filetyper


class ExtractData:
    def __init__(self, filename, converter=27.2113845249047):
        self.filename = filename
        self.contents = filetyper.get_contents(filename)
        self.converter = converter

    def get_charge(self):
        '''
        A function to extract Mulliken Charges from AMS out files
        '''
        symbols = []
        charges = []
        charge_section = filetyper.get_section(self.contents,
                                               "Mulliken Charges",
                                               "Mulliken Shell Charges",
                                               3,
                                               -4)
        for line in charge_section:
            data = line.split()
            symbols.append(data[1])
            charges.append(float(data[2]))
        return symbols, charges

    def get_engine(self):
        '''
        check whether engine is DFTB
        '''
        engine = "Band"
        for line in self.contents:
            if "Engine" in line:
                engine = line.split()[0]
        return engine

    def get_energy(self):
        """
        Function to extract energy from GFN-XTB ams
        """
        energy_data = {}
        energy_section = filetyper.get_section(self.contents,
                                               'Energy Decomposition',
                                               'Gradient Decomposition',
                                               2,
                                               -2)
        for line in energy_section:
            if 'Total Energy (hartree)' in line:
                energy = float(line.split()[3])*self.converter
                energy_data['total_energy_ev'] = energy
            if 'Electronic Energy (hartree)' in line:
                energy = float(line.split()[3])*self.converter
                energy_data['elec_energy_ev'] = energy
            if 'Coulomb Energy (hartree)' in line:
                energy = float(line.split()[3])*self.converter
                energy_data['coulomb_energy_ev'] = energy
            if 'Repulsion Energy (hartree)' in line:
                energy = float(line.split()[3])*self.converter
                energy_data['repulsion_energy_ev'] = energy
            if 'Dispersion Energy (hartree)' in line:
                energy = float(line.split()[3])*self.converter
                energy_data['disp_energy_ev'] = energy
        return energy_data

    def get_cell_volume(self):
        cell_volume_A3 = 0
        for line in self.contents:
            if "Unit cell volume (angstrom^3)" in line:
                cell_volume_A3 = float(line.split()[4])
        return cell_volume_A3




# if __name__ == "__main__":
#     extractor = ExtractData('../example/ABAVOP/ABAVOP.out')
#     extractor.get_cell_volume()

