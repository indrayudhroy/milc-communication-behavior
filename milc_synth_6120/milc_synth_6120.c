#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<time.h>

int NUM_NEIGHBORS = 8;
int neighbors[] = {1, -1, 6, -6, 36, -36, 360, -360};
float global_sum = 0.0;

#define COLLECT_COUNTERS 1

#if COLLECT_COUNTERS
	#include "AriesCounters.h"
	int AC_event_set;
	char** AC_events;
	long long * AC_values;
	int AC_event_count;
	int taskid, numtasks;
	MPI_Comm mod30_comm;

	extern void StartRecordAriesCounters(int my_rank, int reporting_rank_mod, int* AC_event_set, char*** AC_events, long long** AC_values, int* AC_event_count);
	extern void EndRecordAriesCounters(int my_rank, int reporting_rank_mod, double run_time, int* AC_event_set, char*** AC_events, long long** AC_values, int* AC_event_count);	
#endif

int dimMap(int value) {
	switch(value) {
		case -360: return 6120; break;
		case 360: return 6120; break;
		case -36: return 360; break;
		case 36: return 360; break;
		case -6: return 36; break;
		case 6: return 36; break;
		case -1: return 6; break;
		case 1: return 6; break;
	}
}

//Function only works for 204-nodes, 6120 ranks
int findPartnerIndex(int value) {
	switch(value) {
		case 5: return 1; break;
		case 30: return 3; break;
		case 324: return 5; break;
		case 5760: return 7; break;
		case 1: return 0; break;
		case 6: return 2; break;
		case 36: return 4; break;
		case 360: return 6; break;
	}
}

int main(int argc, char const *argv[])
{
	const int DATATYPE_SIZE = 4;
	const int MAX_STREAK = 16;
	const int MPI_ANY_SOURCE_VALUE = -2;
	const int TIMESTEPS = 60;
	const int RANKS_PER_NODE = 30;	

	FILE *fp;
	float local_sum = -1.234;
	int ***table;	
	int i, j, k, blockID, step;
	int myRank, numRanks;
	struct timespec time1, time2;
	int computation_tracker = 0;

	int TOTAL_MPI_CALLS;
	int TOTAL_SENDS_RECVS;
	int TOTAL_ALLREDUCE;
	int TOTAL_CHAINS;	

	fp = fopen("metadata_files/length_meta.q","r");
	fscanf(fp, "%d %d %d %d", &TOTAL_MPI_CALLS, &TOTAL_SENDS_RECVS, &TOTAL_ALLREDUCE, &TOTAL_CHAINS);
	fclose(fp);

	int TOTAL_SLEEP_CALLS = TOTAL_MPI_CALLS - 1;

	int *msgSizeList = malloc(sizeof(int) * TOTAL_SENDS_RECVS);
	fp = fopen("metadata_files/msg_sizes.q","r");
	for (i = 0; i < TOTAL_SENDS_RECVS; i++) {
		fscanf(fp, "%d ", &msgSizeList[i]);
	}
	fclose(fp);

	int *tagList = malloc(sizeof(int) * TOTAL_SENDS_RECVS);
	fp = fopen("metadata_files/taglist.q","r");
	for (i = 0; i < TOTAL_SENDS_RECVS; i++) {
		fscanf(fp, "%d ", &tagList[i]);
	}
	fclose(fp);

	TOTAL_ALLREDUCE++; //Extra termination value

	int *allreduceInstrLocs = malloc(sizeof(int) * TOTAL_ALLREDUCE);
	fp = fopen("metadata_files/allreduce.q","r");
	for (i = 0; i < TOTAL_ALLREDUCE-1; i++) {
		fscanf(fp, "%d ", &allreduceInstrLocs[i]);
	}
	fclose(fp);
	allreduceInstrLocs[i] = -1;

	int *chainLenList = malloc(sizeof(int) * TOTAL_CHAINS);
	fp = fopen("metadata_files/block.dat","r");
	for (i = 0; i < TOTAL_CHAINS; i++) {
		fscanf(fp, "%d ", &chainLenList[i]);
	}
	fclose(fp);

	int *streakLenList = malloc(sizeof(int) * TOTAL_CHAINS);
	fp = fopen("metadata_files/streakValues.dat","r");
	for (i = 0; i < TOTAL_CHAINS; i++) {
		fscanf(fp, "%d ", &streakLenList[i]);
	}
	fclose(fp);

	int *computationTimes = malloc(sizeof(int) * TOTAL_SLEEP_CALLS);
	fp = fopen("metadata_files/comp_times.q","r");
	for (i = 0; i < TOTAL_SLEEP_CALLS; i++) {
		fscanf(fp, "%d ", &computationTimes[i]);
	}
	fclose(fp);


	MPI_Init(NULL, NULL);
	time1.tv_sec = 0; time1.tv_nsec = computationTimes[computation_tracker++]; nanosleep(&time1, &time2);

	MPI_Comm_rank(MPI_COMM_WORLD, &myRank);
	MPI_Comm_size(MPI_COMM_WORLD, &numRanks);

	MPI_Barrier(MPI_COMM_WORLD);			
	time1.tv_sec = 0; time1.tv_nsec = computationTimes[computation_tracker++]; nanosleep(&time1, &time2);

	int myRecvRanks[NUM_NEIGHBORS];
	for (i = 0; i < NUM_NEIGHBORS; i++) {
		int currentNeighbor = neighbors[i];
		int partnerRank = myRank + currentNeighbor;
		int dimension = dimMap(currentNeighbor);
		int lowBound = myRank - (myRank % dimension); 
	    int highBound = lowBound + dimension - 1;
	   
	    if (partnerRank < lowBound || partnerRank > highBound) {
	    	partnerRank = lowBound + (partnerRank % dimension);
	    	// Following only needed without c99 I believe (modulo implementation)
	    	if (partnerRank < 0) {
	    		partnerRank += dimension;
	    	}
	    }
	    myRecvRanks[i] = partnerRank;
	}

	#if COLLECT_COUNTERS
	  /* Initialize for counters collection */
	  // MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
	  // MPI_Comm_rank(MPI_COMM_WORLD, &taskid);

	  // Only want to gather on every 30th rank, so create a new MPI_Group
	  MPI_Group mod30_group, group_world;
	  //int nodeRepeat = 30; //************
	  int numMem = numRanks / RANKS_PER_NODE;
	  int members[numMem];
	  int rank;
	  for (rank=0; rank<numMem; rank++)
	  {
	    members[rank] = rank*RANKS_PER_NODE;
	  }
	  MPI_Comm_group(MPI_COMM_WORLD, &group_world);
	  MPI_Group_incl(group_world, numMem, members, &mod30_group);
	  MPI_Comm_create(MPI_COMM_WORLD, mod30_group, &mod30_comm);

	  // Initialize Papi and counter eventset.
	  InitAriesCounters(argv[0], myRank, RANKS_PER_NODE, &AC_event_set, &AC_events, &AC_values, &AC_event_count);
	#endif		

	// printf("Checkpoint 1.\n");

	// Fill table of partner ranks (specifically partners of Rank0)
    
	FILE *fp2 = fopen("metadata_files/partner.q", "r");

	int total_z_dim = TOTAL_CHAINS;
	int total_x_dim = 0, total_y_dim = 0;

	table = malloc(sizeof(int**) * total_z_dim);

	int z_dim_count = 0;
	
	for (i = 0; i < TOTAL_CHAINS; i++) {
		table[z_dim_count + i] = malloc(sizeof(int *) * chainLenList[i]);
		total_x_dim = total_x_dim + chainLenList[i];
		for (j = 0; j < chainLenList[i]; j++) {
			table[z_dim_count + i][j] = malloc(sizeof(int) * streakLenList[i]);
			total_y_dim = total_y_dim + streakLenList[i];
			for (k = 0; k < streakLenList[i]; k++) {				
				fscanf(fp2, "%d ", &table[z_dim_count + i][j][k]);
			}
			
		}
	}

	fclose(fp2);

	// Each rank updates its lookup table with its partner values (as opposed to Rank0's)

	z_dim_count = 0;
	for (i = 0; i < TOTAL_CHAINS; i++) {
		for (j = 0; j < chainLenList[i]; j++) {
			for (k = 0; k < streakLenList[i]; k++) {
				if (table[z_dim_count+i][j][k] != MPI_ANY_SOURCE_VALUE) {
					int partnerIndex = findPartnerIndex(table[z_dim_count+i][j][k]);
					table[z_dim_count+i][j][k] = myRecvRanks[partnerIndex];				
				}
			}			
		}
	}

	//*********** DEBUG SECTION *************
	//***************************************

	// printf("read okay.\n");

	// int i_count = 0;

	// for (i = 0; i < TOTAL_CHAINS; i++) {	for (j = 0; j < chainLenList[i]; j++) {
	// 		for (k = 0; k < streakLenList[i]; k++) {	printf("%d ", table[i_count + i][j][k]);
	// 		}	printf("\n"); } printf("\n\n"); }
	// printf("**------------------------------\n");
	// printf("**------------------------------\n");

	//******************************************



	int a, b, c;
	int temp, buf_index;
	int recvRank, messageSize, tag, bufCount;
	int **sendBufs = malloc(sizeof(int *) * MAX_STREAK);
	int **recvBufs = malloc(sizeof(int *) * MAX_STREAK);
	MPI_Request *sendReqs = malloc(sizeof(MPI_Request) * MAX_STREAK);
	MPI_Request *recvReqs = malloc(sizeof(MPI_Request) * MAX_STREAK);
	MPI_Status *sendStatus = malloc(sizeof(MPI_Status) * MAX_STREAK);
	MPI_Status *recvStatus = malloc(sizeof(MPI_Status) * MAX_STREAK);	

	int sendrecv_tracker, allreduce_tracker, instructionCount;
	
	//printf("Checkpoint 2.\n");

	for (step = 0; step < TIMESTEPS; step++) {

		#if COLLECT_COUNTERS
			// Start counters collection
			StartRecordAriesCounters(myRank, RANKS_PER_NODE, &AC_event_set, &AC_events, &AC_values, &AC_event_count);
		#endif		

		sendrecv_tracker = 0;
		allreduce_tracker = 0;
		instructionCount = 0;

		instructionCount += 2;	//for init, and 1st barrier		
		computation_tracker = 2;

		// ** BEGIN
		// =============================================================
		z_dim_count = 0;

		for (a = 0; a < TOTAL_CHAINS; a++) {
			for (b = 0; b < chainLenList[a]; b++) {
				for (c = 1; c < streakLenList[a]; c=c+2) {
					recvRank = table[z_dim_count+a][b][c];
					messageSize = msgSizeList[sendrecv_tracker];
					tag = tagList[sendrecv_tracker];
					sendrecv_tracker += 2;

					bufCount = messageSize / DATATYPE_SIZE;
					buf_index = c/2;
					sendBufs[buf_index] = malloc(messageSize);
					recvBufs[buf_index] = malloc(messageSize);
					// bufCount = 25;
					// sendBufs[buf_index] = malloc(100);
					// recvBufs[buf_index] = malloc(100);				

					MPI_Irecv(recvBufs[buf_index], bufCount, MPI_INT, MPI_ANY_SOURCE, tag, MPI_COMM_WORLD, &recvReqs[buf_index]);
					time1.tv_sec = 0; time1.tv_nsec = computationTimes[computation_tracker++]; nanosleep(&time1, &time2);
					MPI_Isend(sendBufs[buf_index], bufCount, MPI_INT, recvRank, tag, MPI_COMM_WORLD, &sendReqs[buf_index]);
					time1.tv_sec = 0; time1.tv_nsec = computationTimes[computation_tracker++]; nanosleep(&time1, &time2);

					instructionCount += 2;

					}
					int streakValue = streakLenList[a] / 2;
					for (temp = 0; temp < streakValue; temp++) {
						MPI_Wait(&recvReqs[temp], &recvStatus[temp]);
						time1.tv_sec = 0; time1.tv_nsec = computationTimes[computation_tracker++]; nanosleep(&time1, &time2);
						MPI_Wait(&sendReqs[temp], &sendStatus[temp]);
						time1.tv_sec = 0; time1.tv_nsec = computationTimes[computation_tracker++]; nanosleep(&time1, &time2);
						free(recvBufs[temp]);
						free(sendBufs[temp]);
						instructionCount += 2;
					}

					if (allreduceInstrLocs[allreduce_tracker] == instructionCount) {				
						do {
							MPI_Allreduce(&local_sum, &global_sum, 1, MPI_FLOAT, MPI_SUM, MPI_COMM_WORLD);
							time1.tv_sec = 0; time1.tv_nsec = computationTimes[computation_tracker++]; nanosleep(&time1, &time2);
							allreduce_tracker++;
							instructionCount++;
						}
						while (allreduceInstrLocs[allreduce_tracker] == allreduceInstrLocs[allreduce_tracker-1] + 1);
					}

					//free if needed
			}	//end of b
			//free if needed
		}	//end of a
		//free if needed

		MPI_Barrier(MPI_COMM_WORLD);
		time1.tv_sec = 0; time1.tv_nsec = computationTimes[computation_tracker++]; nanosleep(&time1, &time2);

		#if COLLECT_COUNTERS
			EndRecordAriesCounters(myRank, RANKS_PER_NODE, 123.456, &AC_event_set, &AC_events, &AC_values, &AC_event_count);
		#endif		
	}

	#if COLLECT_COUNTERS
	  /* Cleanup for counters collection */
	  FinalizeAriesCounters(&mod30_comm, myRank, RANKS_PER_NODE, &AC_event_set, &AC_events, &AC_values, &AC_event_count);
	#endif 	

	MPI_Finalize();

	instructionCount += 2;

	if (myRank == 0) {
		fp = fopen("ending.log", "w");
		fprintf(fp, "Ending log\n----------\nSendrecv_tracker = %d\n", sendrecv_tracker);
		fprintf(fp, "instr count = %d\n", instructionCount);
		fprintf(fp, "comp. count = %d\n", computation_tracker);
		fprintf(fp, "allreduce_tracker = %d\n", allreduce_tracker);
		// fprintf(fp, "count = %d, count2 = %d\n", debug_count,debug_count2);
		fclose(fp);
	}	

	return 0;

}