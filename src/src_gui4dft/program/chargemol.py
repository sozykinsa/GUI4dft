from core_atomistic.atomic_model import AtomicModel


def get_charges_ddec6(file, model: AtomicModel):
    f = open(file)
    n_str = f.readline()
    f.readline()
    str1 = f.readline().split()
    if len(str1) == 5:
        n = int(n_str)
        if n == model.n_atoms():
            for i in range(n):
                model.atoms[i].set_property("DDEC6", float(str1[4]))
                str1 = f.readline().split()
        else:
            print("Error in reading charges for ", model.n_atoms(), " atoms")
    else:
        print("Error in reading charges")
    f.close()
