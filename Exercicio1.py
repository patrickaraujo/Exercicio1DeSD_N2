from mpi4py import MPI
import datetime


def calSomatorio(inicio, fim):
    s = 0
    for i in range(inicio, fim + 1):
        s = s + i

    return s

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    size = comm.Get_size()  #   n
    rank = comm.Get_rank()  # id
    start_time = datetime.datetime.now()
    print('size=%d, rank = %d' % (size, rank))

    num = 0;

    if rank == 0:
        print("Digite o numero desejado: ")
        num = int(input())
        for i in range(1, size-1):
            comm.send(num, dest=i, tag=1)
    else:
        val = comm.recv(source=0, tag=1)

    # total = 0
    somatorio = soma = 0

    parcela = (int)(num/size)
    inicio = (parcela*rank)+1
    fim = parcela*(rank+1)

    if(rank == size-1):
        fim = num

    somatorio = calSomatorio(inicio, fim)


    metade = size

    while True:
        metade = metade/2
        soma = somatorio
        if rank >= metade:
            # if rank == rank + half:
            #     break
            comm.send(soma, dest=rank-metade, tag=2)
            print(" %d - Envia: %2.3f " % (rank-metade, soma))
        else:
            soma = comm.recv(source=rank+metade, tag=2)
            #   integral    somatoria
            #   integral = total + integral
            somatorio = somatorio + soma
            print(" %d - Recebe: %2.3f " % (rank+metade, soma))
        if ((rank < metade) and (metade > 1)):
            break

    if rank == 0:
        end_time = datetime.datetime.now()
        time_diff = (end_time - start_time)
        execution_time = time_diff.total_seconds()
        print("\n Result: ", somatorio)
        print("Run time in clock seconds: %.20lf " % (execution_time))