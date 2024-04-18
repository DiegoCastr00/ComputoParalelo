# Import the necessary dependencies
import torchvision.transforms as transforms
import medmnist
from medmnist import INFO
import numpy as np
import multiprocessing
import time
import datetime
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Load the dataset
data_flag = "breastmnist"

download = True

info = INFO[data_flag]
DataClass = getattr(medmnist, info["python_class"])

# preprocessing
data_transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize(mean=[0.5], std=[0.5])]
)

# load the data
train_dataset = DataClass(split="train", transform=data_transform, download=download)
test_dataset = DataClass(split="test", transform=data_transform, download=download)

# Convierte los DataLoaders a listas de imágenes y etiquetas
train_images = [image for image, label in train_dataset]
train_labels = [label for image, label in train_dataset]
test_images = [image for image, label in test_dataset]
test_labels = [label for image, label in test_dataset]

# Convierte las listas a arrays de numpy
train_images = np.array(train_images)
train_labels = np.array(train_labels)
test_images = np.array(test_images)
test_labels = np.array(test_labels)

# Se aplana las imágenes ya que los clasificadores no aceptan imágenes en 2D
# entonces se convierten a vectores de 1D
X_train = train_images.reshape((train_images.shape[0], -1))
X_test = test_images.reshape((test_images.shape[0], -1))
y_train = train_labels.reshape((train_labels.shape[0], -1))
y_train = np.squeeze(y_train)
y_test = test_labels.reshape((test_labels.shape[0], -1))
y_test = np.squeeze(y_test)

# We create a list with the parameters to be evaluated
hyperparameters = []
for criterion in ["gini", "entropy", "log_loss"]:
    for trees in range(5, 10):  # Número de árboles (de 5 a 10, en este caso)
        for max_features in range(
            500, 784
        ):  # Número de atributos (max features = 784, no puede excederlo)
            for max_samples in range(
                10, 120, 10
            ):  # Número de instancias (No puede exceder al # de instancias en el dataset)(de [10,120] de 10 en 10)
                hyperparameters.append([trees, max_features, max_samples, criterion])


def evaluate_set(hyperparameter_set, results, lock, i):
    """
    Evaluate a set of hyperparameters
    Args:
    hyperparameter_set: a list with the set of hyperparameters to be evaluated
    results: a shared list to store the evaluation results
    """
    print("\n Yo soy el proceso:", i, "Comence a las:", datetime.datetime.now())

    # Hyperparameter to use
    for s in hyperparameter_set:
        clf = RandomForestClassifier(
            n_estimators=int(s[0]),
            max_features=int(s[1]),
            max_samples=int(s[2]),
            criterion=s[3],
        )
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        with lock:
            print(
                f"Proceso {i} con parametros {s} y accuracy {accuracy_score(y_test,y_pred)}"
            )
            results.append(accuracy_score(y_test, y_pred))


def main():

    # Initialize shared data structures
    manager = multiprocessing.Manager()
    results = manager.list()

    # Now we will evaluate with multiple processes
    processes = []
    N_PROCESSES = 4
    splits = np.array_split(hyperparameters, N_PROCESSES)
    lock = multiprocessing.Lock()

    start_time = time.perf_counter()

    for i in range(N_PROCESSES):
        # Generate the processing threads
        p = multiprocessing.Process(
            target=evaluate_set, args=(splits[i], results, lock, i)
        )
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Time
    finish_time = time.perf_counter()
    print(f"Program finished in {finish_time-start_time} seconds")

    # Process the results
    print("Results:")
    for i, acc in enumerate(results):
        print(f"Accuracy for process {i}: {acc}")


if __name__ == "__main__":
    main()
